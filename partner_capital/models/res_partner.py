# -*- coding: utf-8 -*-
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    capital_country_id = fields.Many2one(
        'res.country',
        "Capital country",
        oldname="capital_country",
        help="Country of origin of this company's capital.")
    capital_amount = fields.Float(
        "Capital amount",
        oldname="capital_registered",
        help="Publicly registered capital amount.")
    capital_currency_id = fields.Many2one(
        "res.currency",
        string="Capital currency")
    turnover_range_id = fields.Many2one(
        'res.partner.turnover_range',
        "Turnover range",
        oldname="turnover_range")
    turnover_amount = fields.Float(
        oldname="turnover_number")
    company_size = fields.Selection(
        string="Company size",
        selection=[('micro', 'Micro'), ('small', 'Small'),
                   ('medium', 'Medium'), ('big', 'Big')])
