# -*- coding: utf-8 -*-
# © 2013-2017 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later <http://www.gnu.org/licenses/agpl.html>.
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools import drop_view_if_exists
from .res_partner_relation_type_selection import _RECORD_TYPES


class ResPartnerRelationAll(Model):
    _auto = False
    _log_access = False
    _name = 'res.partner.relation.all'
    _description = 'All (non-inverse + inverse) relations between partners'

    _additional_view_fields = []
    """append to this list if you added fields to res_partner_relation that
    you need in this model and related fields are not adequate (ie for sorting)
    You must use the same name as in res_partner_relation.
    Don't overwrite this list in your declatarion but append in _auto_init:

    def _auto_init(self, cr, context=None):
        self._additional_view_fields.append('my_field')
        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    _columns = {
        'my_field': ....
    }
    """

    def _auto_init(self, cr, context=None):
        """Create view instead of table."""
        drop_view_if_exists(cr, self._table)
        additional_view_fields = ','.join(self._additional_view_fields)
        additional_view_fields = (',' + additional_view_fields)\
            if additional_view_fields else ''
        cr.execute(
            """create or replace view %s as
            select
                id * 10 as id,
                id as relation_id,
                type_id,
                cast('a' as char(1)) as record_type,
                left_partner_id as this_partner_id,
                right_partner_id as other_partner_id,
                date_start,
                date_end,
                active,
                type_id * 10 as type_selection_id
                %s
            from res_partner_relation
            union select
                id * 10 + 1,
                id,
                type_id,
                cast('b' as char(1)),
                right_partner_id,
                left_partner_id,
                date_start,
                date_end,
                active,
                type_id * 10 + 1
                %s
            from res_partner_relation
            """,
            params=(
                self._table,
                additional_view_fields,
                additional_view_fields,
            )
        )
        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    _columns = {
        'record_type': fields.selection(
            _RECORD_TYPES,
            'Record type',
            readonly=True,
        ),
        'relation_id': fields.many2one(
            'res.partner.relation', 'Relation', readonly=True),
        'type_id': fields.many2one(
            'res.partner.relation.type', 'Relation type', readonly=True),
        'type_selection_id': fields.many2one(
            'res.partner.relation.type.selection', 'Relation type',
            readonly=True),
        'this_partner_id': fields.many2one(
            'res.partner', 'Current partner', readonly=True),
        'other_partner_id': fields.many2one(
            'res.partner', 'Other partner', readonly=True),
        'date_start': fields.date('Starting date'),
        'date_end': fields.date('Ending date'),
        'active': fields.boolean('Active'),
    }

    def name_get(self, cr, uid, ids, context=None):
        """Create name from both partners and relation."""
        return dict([
            (this.id, '%s %s %s' % (
                this.this_partner_id.name,
                this.type_selection_id.name_get()[0][1],
                this.other_partner_id.name,
            ))
            for this in self.browse(cr, uid, ids, context=context)])

    def write(self, cr, uid, ids, vals, context=None):
        """divert non-problematic writes to underlying table"""
        # pylint: disable=W8106
        return self.pool['res.partner.relation'].write(
            cr, uid,
            [i / 10 for i in ids],
            dict([(k, vals[k])
                  for k in vals
                  if not self._columns[k].readonly]),
            context=context)
