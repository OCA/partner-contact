# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if 'customer' in vals and vals.get('customer'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'res.partner.customer')

        return super(ResPartner, self).create(vals)
