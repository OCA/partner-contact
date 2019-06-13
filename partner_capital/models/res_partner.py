# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    capital_country_id = fields.Many2one(
        'res.country',
        "Capital country",
        help="Country of origin of this company's capital.")
    capital_amount = fields.Monetary(
        "Capital amount",
        currency_field='capital_currency_id',
        help="Publicly registered capital amount.")
    capital_currency_id = fields.Many2one(
        "res.currency",
        string="Capital currency")
    turnover_range_id = fields.Many2one(
        'res.partner.turnover_range',
        "Turnover range")
    turnover_amount = fields.Float()
    company_size = fields.Selection(
        string="Company size",
        selection=[('micro', 'Micro'), ('small', 'Small'),
                   ('medium', 'Medium'), ('big', 'Big')])
