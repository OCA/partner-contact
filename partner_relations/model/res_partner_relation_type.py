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

from openerp import models, fields, api, _


class ResPartnerRelationType(models.Model):
    """Model that defines relation types that might exist between partners"""
    _name = 'res.partner.relation.type'
    _description = 'Partner Relation Type'
    _order = 'name'

    name = fields.Char(
        'Name',
        size=128,
        required=True,
        translate=True,
    )
    name_inverse = fields.Char(
        'Inverse name',
        size=128,
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
        'Allow both sides to be the same',
        default=False,
    )

    @api.model
    def _get_partner_types(self):
        return [
            ('c', _('Company')),
            ('p', _('Person')),
        ]
