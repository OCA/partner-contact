# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PartnerPriority(models.Model):
    _name = 'partner.priority'
    _order = 'sequence'
    _description = 'Partner Priority'

    name = fields.Char(string="Priority", required=True)
    description = fields.Text(required=True)
    sequence = fields.Integer(required=True, default=lambda self: self.env[
        'ir.sequence'].next_by_code('res.partner.priority') or 0)
