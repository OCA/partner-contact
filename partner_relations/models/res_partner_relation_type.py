# -*- coding: utf-8 -*-
# © 2013-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api, _


class ResPartnerRelationType(models.Model):
    """Model that defines relation types that might exist between partners"""
    _name = 'res.partner.relation.type'
    _description = 'Partner Relation Type'
    _order = 'name'

    name = fields.Char(
        'Name',
        required=True,
        translate=True,
    )
    name_inverse = fields.Char(
        'Inverse name',
        required=True,
        translate=True,
    )
    contact_type_left = fields.Selection(
        '_get_partner_types',
        'Left partner type',
    )
    contact_type_right = fields.Selection(
        '_get_partner_types',
        'Right partner type',
    )
    partner_category_left = fields.Many2one(
        'res.partner.category',
        'Left partner category',
    )
    partner_category_right = fields.Many2one(
        'res.partner.category',
        'Right partner category',
    )
    allow_self = fields.Boolean(
        'Reflexive',
        help='This relation can be set up with the same partner left and '
        'right',
        default=False,
    )
    symmetric = fields.Boolean(
        'Symmetric',
        help='This relation is the same from right to left as from left to '
        'right',
        default=False,
    )

    @api.model
    def _get_partner_types(self):
        return [
            ('c', _('Company')),
            ('p', _('Person')),
        ]

    @api.onchange('symmetric')
    def _onchange_symmetric(self):
        self.update({
            'name_inverse': self.name,
            'contact_type_right': self.contact_type_left,
            'partner_category_right': self.partner_category_left,
        })
