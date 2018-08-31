# -*- coding: utf-8 -*-
# Copyright 2013-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later <http://www.gnu.org/licenses/agpl.html>.
import time

from openerp.osv import orm, fields
from openerp.osv.expression import is_leaf, AND, OR, FALSE_LEAF
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def _get_relation_ids_select_select(self, field_name=None):
        return "SELECT rpr.id, rpr.left_partner_id, rpr.right_partner_id"

    def _get_relation_ids_select_from(self, field_name=None):
        return "FROM res_partner_relation rpr"

    def _get_relation_ids_select_where(self, field_name=None):
        return \
            "WHERE (rpr.left_partner_id IN %s OR rpr.right_partner_id IN %s)"

    def _get_relation_ids_select_order_by(self, field_name=None):
        return "ORDER BY %s" % self.pool['res.partner.relation']._order

    def _get_relation_ids_select(
            self, cr, uid, ids, field_name, arg, context=None):
        """Return the relation id's for field_name."""
        # No real danger here for SQL injection.
        # pylint: disable=sql-injection
        statement = (
            "%(select)s %(from)s %(where)s %(order_by)s" % {
                'select': self._get_relation_ids_select_select(
                    field_name=field_name),
                'from': self._get_relation_ids_select_from(
                    field_name=field_name),
                'where': self._get_relation_ids_select_where(
                    field_name=field_name),
                'order_by': self._get_relation_ids_select_order_by(
                    field_name=field_name)})
        cr.execute(statement, (tuple(ids), tuple(ids)))
        return cr.fetchall()

    def _get_relation_ids(
            self, cr, uid, ids, field_name, arg, context=None):
        """getter for relation_ids"""
        if context is None:
            context = {}
        result = dict([(i, []) for i in ids])
        # TODO: do a permission test on returned ids
        for row in self._get_relation_ids_select(
                cr, uid, ids, field_name, arg, context=context):
            if row[1] in result:
                result[row[1]].append(row[0])
            if row[2] in result:
                result[row[2]].append(row[0])
        return result

    def _set_relation_ids(
            self, cr, uid, ids, dummy_name, field_value, dummy_arg,
            context=None):
        """setter for relation_ids"""
        if context is None:
            context = {}
        relation_obj = self.pool.get('res.partner.relation')
        context2 = self._update_context(context, ids)
        for value in field_value:
            if value[0] == 0:
                relation_obj.create(cr, uid, value[2], context=context2)
            if value[0] == 1:
                # if we write partner_id_display, we also need to pass
                # type_selection_id in order to have this write end up on
                # the correct field
                if 'partner_id_display' in value[2] and 'type_selection_id'\
                        not in value[2]:
                    relation_data = relation_obj.read(
                        cr, uid, [value[1]], ['type_selection_id'],
                        context=context)[0]
                    value[2]['type_selection_id'] =\
                        relation_data['type_selection_id']
                relation_obj.write(
                    cr, uid, value[1], value[2], context=context2)
            if value[0] == 2:
                relation_obj.unlink(cr, uid, value[1], context=context2)

    def _search_relation_id(
            self, cr, uid, dummy_obj, name, args, context=None):
        result = []
        for arg in args:
            if isinstance(arg, tuple) and arg[0] == name:
                if arg[1] not in ['=', '!=', 'like', 'not like', 'ilike',
                                  'not ilike', 'in', 'not in']:
                    raise orm.except_orm(
                        _('Error'),
                        _('Unsupported search operand "%s"') % arg[1])

                relation_type_selection_ids = []
                relation_type_selection = self\
                    .pool['res.partner.relation.type.selection']

                if arg[1] == '=' and isinstance(arg[2], (long, int)):
                    relation_type_selection_ids.append(arg[2])
                elif arg[1] == '!=' and isinstance(arg[2], (long, int)):
                    type_id, is_inverse = relation_type_selection\
                        .get_type_from_selection_id(
                            cr, uid, arg[2])
                    result = OR([
                        result,
                        [
                            ('relation_all_ids.type_id', '!=', type_id),
                        ]
                    ])
                    continue
                else:
                    relation_type_selection_ids = relation_type_selection\
                        .search(
                            cr, uid,
                            [
                                ('type_id.name', arg[1], arg[2]),
                                ('record_type', '=', 'a'),
                            ],
                            context=context)
                    relation_type_selection_ids.extend(
                        relation_type_selection.search(
                            cr, uid,
                            [
                                ('type_id.name_inverse', arg[1], arg[2]),
                                ('record_type', '=', 'b'),
                            ],
                            context=context))

                if not relation_type_selection_ids:
                    result = AND([result, [FALSE_LEAF]])

                for relation_type_selection_id in relation_type_selection_ids:
                    type_id, is_inverse = relation_type_selection\
                        .get_type_from_selection_id(
                            cr, uid, relation_type_selection_id)

                    result = OR([
                        result,
                        [
                            '&',
                            ('relation_all_ids.type_id', '=', type_id),
                            ('relation_all_ids.record_type', '=',
                             'b' if is_inverse else 'a')
                        ],
                    ])

        return result

    def _search_relation_date(self, cr, uid, obj, name, args, context=None):
        result = []
        for arg in args:
            if isinstance(arg, tuple) and arg[0] == name:
                # TODO: handle {<,>}{,=}
                if arg[1] != '=':
                    continue

                result.extend([
                    '&',
                    '|',
                    ('relation_all_ids.date_start', '=', False),
                    ('relation_all_ids.date_start', '<=', arg[2]),
                    '|',
                    ('relation_all_ids.date_end', '=', False),
                    ('relation_all_ids.date_end', '>=', arg[2]),
                ])

        return result

    def _search_related_partner_id(
            self, cr, uid, dummy_obj, name, args, context=None):
        result = []
        for arg in args:
            if isinstance(arg, tuple) and arg[0] == name:
                result.append(
                    (
                        'relation_all_ids.other_partner_id',
                        arg[1],
                        arg[2],
                    ))

        return result

    def _search_related_partner_category_id(
            self, cr, uid, dummy_obj, name, args, context=None):
        result = []
        for arg in args:
            if isinstance(arg, tuple) and arg[0] == name:
                result.append(
                    (
                        'relation_all_ids.other_partner_id.category_id',
                        arg[1],
                        arg[2],
                    ))

        return result

    _columns = {
        'relation_ids': fields.function(
            lambda self, *args, **kwargs: self._get_relation_ids(
                *args, **kwargs),
            fnct_inv=_set_relation_ids,
            type='one2many', obj='res.partner.relation',
            string='Relations',
            selectable=False,
        ),
        'relation_all_ids': fields.one2many(
            'res.partner.relation.all', 'this_partner_id',
            string='All relations with current partner',
            auto_join=True,
            selectable=False,
        ),
        'search_relation_id': fields.function(
            lambda self, cr, uid, ids, *args: dict([
                (i, False) for i in ids]),
            fnct_search=_search_relation_id,
            string='Has relation of type',
            type='many2one', obj='res.partner.relation.type.selection'
        ),
        'search_relation_partner_id': fields.function(
            lambda self, cr, uid, ids, *args: dict([
                (i, False) for i in ids]),
            fnct_search=_search_related_partner_id,
            string='Has relation with',
            type='many2one', obj='res.partner'
        ),
        'search_relation_date': fields.function(
            lambda self, cr, uid, ids, *args: dict([
                (i, False) for i in ids]),
            fnct_search=_search_relation_date,
            string='Relation valid', type='date'
        ),
        'search_relation_partner_category_id': fields.function(
            lambda self, cr, uid, ids, *args: dict([
                (i, False) for i in ids]),
            fnct_search=_search_related_partner_category_id,
            string='Has relation with a partner in category',
            type='many2one', obj='res.partner.category'
        ),
    }

    def copy_data(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.setdefault('relation_ids', [])
        default.setdefault('relation_all_ids', [])
        return super(ResPartner, self).copy_data(cr, uid, id, default=default,
                                                 context=context)

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        if context is None:
            context = {}
        # inject searching for current relation date if we search for relation
        # properties and no explicit date was given
        date_args = []
        for arg in args:
            if is_leaf(arg) and arg[0].startswith('search_relation'):
                if arg[0] == 'search_relation_date':
                    date_args = []
                    break
                if not date_args:
                    date_args = [
                        ('search_relation_date', '=', time.strftime(
                            DEFAULT_SERVER_DATE_FORMAT))]

        # because of auto_join, we have to do the active test by hand
        active_args = []
        if context.get('active_test', True):
            for arg in args:
                if is_leaf(arg) and\
                        arg[0].startswith('search_relation'):
                    active_args = [('relation_all_ids.active', '=', True)]
                    break

        return super(ResPartner, self).search(
            cr, uid, args + date_args + active_args, offset=offset,
            limit=limit, order=order, context=context, count=count)

    def read(
            self, cr, uid, ids, fields=None, context=None,
            load='_classic_read'):
        return super(ResPartner, self).read(
            cr, uid, ids, fields=fields,
            context=self._update_context(context, ids), load=load)

    def write(self, cr, uid, ids, vals, context=None):
        return super(ResPartner, self).write(
            cr, uid, ids, vals, context=self._update_context(context, ids))

    def _update_context(self, context, ids):
        if context is None:
            context = {}
        ids = ids if isinstance(ids, list) else [ids] if ids else []
        result = context.copy()
        result.setdefault('active_id', ids[0] if ids else None)
        result.setdefault('active_ids', ids)
        result.setdefault('active_model', self._name)
        return result
