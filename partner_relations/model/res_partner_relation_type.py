# -*- coding: utf-8 -*-
'''Define model res.partner.relation.type'''
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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


class ResPartnerRelationType(Model):
    '''Model that defines relation types that might exist between partners'''
    _name = 'res.partner.relation.type'
    _description = 'Parter relation type'
    _order = 'name'

    def _get_partner_types(self, cr, uid, context=None):
        return (('c', 'Company'), ('p', 'Person'),)

    _columns = {
        'name': fields.char(
            'Name', size=128, required=True, translate=True),
        'name_inverse': fields.char(
            'Inverse name', size=128, required=True, translate=True),
        'contact_type_left': fields.selection(
            _get_partner_types, 'Left partner type'),
        'contact_type_right': fields.selection(
            _get_partner_types, 'Right partner type'),
        'partner_category_left': fields.many2one(
            'res.partner.category', 'Left partner category'),
        'partner_category_right': fields.many2one(
            'res.partner.category', 'Right partner category'),
    }
