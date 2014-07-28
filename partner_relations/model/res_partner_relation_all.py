# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools import drop_view_if_exists
from res_partner_relation_type_selection import ResPartnerRelationTypeSelection


class ResPartnerRelationAll(Model):
    _auto = False
    _log_access = False
    _name = 'res.partner.relation.all'
    _description = 'All (non-inverse + inverse) relations between partners'

    def _auto_init(self, cr, context=None):
        drop_view_if_exists(cr, self._table)
        cr.execute(
            '''create or replace view %s as
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
             from res_partner_relation''' % self._table)

        return super(ResPartnerRelationAll, self)._auto_init(
            cr, context=context)

    _columns = {
        'record_type': fields.selection(
            ResPartnerRelationTypeSelection._RECORD_TYPES, 'Record type'),
        'relation_id': fields.many2one(
            'res.partner.relation', 'Relation'),
        'type_id': fields.many2one(
            'res.partner.relation.type', 'Relation type'),
        'type_selection_id': fields.many2one(
            'res.partner.relation.type.selection', 'Relation type'),
        'this_partner_id': fields.many2one('res.partner', 'Current partner'),
        'other_partner_id': fields.many2one('res.partner', 'Other partner'),
        'date_start': fields.date('Starting date'),
        'date_end': fields.date('Ending date'),
        'active': fields.boolean('Active'),
    }

    def name_get(self, cr, uid, ids, context=None):
        return dict([
            (this.id, '%s %s %s' % (
                this.this_partner_id.name,
                this.type_selection_id.name_get()[0][1],
                this.other_partner_id.name,
            ))
            for this in self.browse(cr, uid, ids, context=context)])
