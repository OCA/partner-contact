# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartnerAlias(models.Model):

    _inherits = {'res.partner': 'partner_id'}
    _name = 'res.partner.alias'
    _description = 'Res Partner Alias'

    partner_id = fields.Many2one(
        string='Related Partner',
        comodel_name='res.partner',
        required=True,
        ondelete='cascade',
        index=True,
    )
    firstname = fields.Char(
        string='First Name',
        required=True,
    )

    @api.multi
    @api.constrains('firstname')
    def _check_firstname(self):
        for record in self:
            if record.firstname == record.partner_id.firstname:
                raise ValidationError(_(
                    'Alias first name cannot be the same as '
                    'primary firstname'
                ))

    _sql_constraints = [
        ('alias_name_uniq',
         'UNIQUE(firstname)',
         'Alias first name must be unique'),
    ]
