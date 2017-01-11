# -*- coding: utf-8 -*-
# © 2013-2017 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later <http://www.gnu.org/licenses/agpl.html>.
from openerp.osv.orm import Model
from openerp.osv import fields


class ResPartnerRelationType(Model):
    """Model that defines relation types that might exist between partners"""
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
