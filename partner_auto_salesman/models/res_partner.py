# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one('res.users',
                              string='Salesperson',
                              help='The internal user that is in charge of'
                                   'communicating with this contact if any.',
                              default=lambda self: self.env.uid)
