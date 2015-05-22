# -*- coding: utf-8 -*-
##############################################################################
#
#    Contributor:   David Dufresne <david.dufresne@savoirfairelinux.com>
#                   Sandy Carter <sandy.carter@savoirfairelinux.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import pooler, SUPERUSER_ID
from itertools import groupby
from operator import attrgetter


def remove_sql_constraint_duplicates(cr, model, constraint_attrs):
    """
    This function was copied from OpenUpgrade

    Remove all duplicates after a sql constraint is applied on a model.

    For every field many2one and many2many with the given model as relation,
    change the duplicate ids with the id of the record kept.

    This script must be called in post-migration so that the model being
    edited can be accessed through the orm.

    When upgrading the module, if there are duplicates, integrity errors
    will be raised before the script is run but this will not prevent
    the script from running.

    :param model: the model on witch the constraint is applied
    :param constraint_attrs: a list of string containing the fields that
                                form the uniq key
    """
    pool = pooler.get_pool(cr.dbname)
    model_pool = pool[model]
    model_table = model_pool._table

    # Get all fields with the given model as many2one relation
    field_pool = pool['ir.model.fields']
    field_m2o_ids = field_pool.search(cr, SUPERUSER_ID, [
        ('relation', '=', model),
        ('ttype', '=', 'many2one'),
    ])
    # List of tables where to look for duplicates
    # This is trivial for many2one relations
    tables_to_lookup = [
        (
            pool[field.model_id.model]._table,
            field.name, 'many2one'
        ) for field in field_pool.browse(cr, SUPERUSER_ID, field_m2o_ids)
    ]

    # For many2many relations, we need to check over the existing
    # foreign keys in the database in order to find the tables

    # Get all fields with the given model as many2many relation
    field_m2m_ids = field_pool.search(cr, SUPERUSER_ID, [
        ('relation', '=', model),
        ('ttype', '=', 'many2many'),
    ])
    fields_m2m = field_pool.browse(cr, SUPERUSER_ID, field_m2m_ids)

    for field in fields_m2m:

        other_model_table = pool[field.model_id.model]._table

        # Get all primary key constraints for the given table
        query = "SELECT " \
            "    tc.table_name, kcu.column_name, ccu.table_name " \
            "FROM " \
            "    information_schema.table_constraints AS tc " \
            "    JOIN information_schema.key_column_usage AS kcu " \
            "        ON tc.constraint_name = kcu.constraint_name " \
            "    JOIN information_schema.constraint_column_usage AS ccu " \
            "        ON ccu.constraint_name = tc.constraint_name " \
            "WHERE constraint_type = 'FOREIGN KEY' " \
            "        and ccu.table_name " \
            "        in ('%(model_table)s', '%(other_model_table)s') " \
            " ORDER BY tc.table_name;" % {
                'model_table': model_table,
                'other_model_table': other_model_table
            }

        cr.execute(query)
        for key, group in groupby(cr.fetchall(), key=lambda c: c[0]):
            constraints = list(group)

            model_field = next(
                (c[1] for c in constraints if c[2] == model_table), False)
            other_field = next(
                (c[1] for c in constraints if c[2] == other_model_table), False
            )

            if model_field and other_field:
                # Add the current table to the list of tables where to look
                # for duplicates
                tables_to_lookup.append((
                    key, model_field, 'many2many', other_field))

    # Get all records
    record_ids = model_pool.search(cr, SUPERUSER_ID, [])
    records = model_pool.browse(cr, SUPERUSER_ID, record_ids)

    # Sort records by the constraint attributes
    # so that they can be grouped with itertools.groupby
    records.sort(key=attrgetter(*constraint_attrs))

    for key, group in groupby(records, key=lambda x: tuple(
        x[attr] for attr in constraint_attrs)
    ):
        grouped_records = list(group)

        if len(grouped_records) > 1:
            # Define a record to keep
            new_record_id = grouped_records[0].id

            # All other records are to remove
            old_record_ids = [z.id for z in grouped_records[1:]]

            all_record_ids = old_record_ids + [new_record_id]

            # Replace every many2one record in the database that has an old
            # record as value with the record to keep

            for table in tables_to_lookup:
                table_name = table[0]

                # Prevent the upgrade script to create duplicates
                # in the many2many relation table and raise a constraint error
                if table[2] == 'many2many':
                    cr.execute(
                        "   SELECT t.%(other_field)s, t.%(field_name)s "
                        "   FROM %(table_name)s as t"
                        "   WHERE %(field_name)s "
                        "   in %(all_record_ids)s "
                        "   ORDER BY %(other_field)s" %
                        {
                            'table_name': table_name,
                            'field_name': table[1],
                            'other_field': table[3],
                            'all_record_ids': tuple(all_record_ids),
                        })

                    for k, group_to_check in groupby(
                        cr.fetchall(), lambda rec: rec[0]
                    ):
                        group_to_check = list(group_to_check)
                        if len(group_to_check) > 1:
                            for rec_to_unlink in group_to_check[1:]:
                                cr.execute(
                                    "   DELETE FROM %(table_name)s "
                                    "   WHERE %(field_name)s = %(field_value)s"
                                    "   AND %(other_field)s "
                                    "   = %(other_field_value)s" %
                                    {
                                        'table_name': table_name,
                                        'field_name': table[1],
                                        'field_value': rec_to_unlink[1],
                                        'other_field': table[3],
                                        'other_field_value': rec_to_unlink[0],
                                    })

                # Main upgrade script
                cr.execute(
                    "   UPDATE %(table_name)s"
                    "   SET %(field_name)s = %(new_value)s"
                    "   WHERE %(field_name)s %(old_record_ids)s;" %
                    {
                        'table_name': table_name,
                        'field_name': table[1],
                        'new_value': new_record_id,
                        'old_record_ids': len(old_record_ids) > 1 and
                        'in %s' % (tuple(old_record_ids),) or '= %s' %
                        old_record_ids[0]
                    })

            model_pool.unlink(cr, SUPERUSER_ID, old_record_ids)


def migrate(cr, version):
    """
    Remove duplicated locations
    """
    if not version:
        return

    constraint_attrs = ['name', 'city', 'state_id', 'country_id']
    remove_sql_constraint_duplicates(
        cr, 'res.better.zip', constraint_attrs)
