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
from openerp import SUPERUSER_ID


class ResPartnerRelationType(Model):
    _inherit = 'res.partner.relation.type'

    _columns = {
        'own_tab_left': fields.boolean('Show in own tab'),
        'own_tab_right': fields.boolean('Show in own tab'),
    }

    _defaults = {
        'own_tab_left': False,
        'own_tab_right': False,
    }

    def _update_res_partner_fields(self, cr):
        field_name_prefix = 'relation_ids_own_tab_'
        field_name_format = field_name_prefix + '%s_%s'
        res_partner = self.pool['res.partner']
        for field_name in res_partner._columns.copy():
            if field_name.startswith(field_name_prefix):
                del res_partner._columns[field_name]

        def add_field(relation, inverse):
            field = fields.one2many(
                'res.partner.relation',
                '%s_partner_id' % ('left' if not inverse else 'right'),
                string=relation['name' if not inverse else 'name_inverse'],
                domain=[('type_id', '=', relation.id),
                        '|',
                        ('active', '=', True),
                        ('active', '=', False)])
            field_name = field_name_format % (
                relation.id,
                'left' if not inverse else 'right')
            res_partner._columns[field_name] = field

        for relation in self.browse(
                cr, SUPERUSER_ID,
                self.search(
                    cr, SUPERUSER_ID,
                    [
                        '|',
                        ('own_tab_left', '=', True),
                        ('own_tab_right', '=', True),
                    ])):
            if relation.own_tab_left:
                add_field(relation, False)
            if relation.own_tab_right:
                add_field(relation, True)

    def _register_hook(self, cr):
        self._update_res_partner_fields(cr)

    def create(self, cr, uid, vals, context=None):
        result = super(ResPartnerRelationType, self).create(
            cr, uid, vals, context=context)
        if vals.get('own_tab_left') or vals.get('own_tab_right'):
            self._update_res_partner_fields(cr)
        return result

    def write(self, cr, uid, ids, vals, context=None):
        result = super(ResPartnerRelationType, self).write(
            cr, uid, ids, vals, context=context)
        if 'own_tab_left' in vals or 'own_tab_right' in vals:
            self._update_res_partner_fields(cr)
        return result
