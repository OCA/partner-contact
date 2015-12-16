# -*- coding: utf-8 -*-
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    capital_country = fields.Many2one(
        'res.country',
        "Capital country",
        help="Country of origin of this company's capital.")
    capital_amount = fields.Float(
        "Capital amount",
        help="Publicly registered capital amount.")
    turnover_range_id = fields.Many2one(
        'res.partner.turnover_range',
        "Turnover range")
    turnover_amount = fields.Float()
    company_size = fields.Selection(
        string="Company size",
        selection=[('micro', 'Micro'), ('small', 'Small'),
                   ('medium', 'Medium'), ('big', 'Big')])
