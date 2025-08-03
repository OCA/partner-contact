# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2015 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    capital_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Capital country",
        help="Country of origin of this company's capital.",
    )
    capital_amount = fields.Monetary(
        string="Capital amount",
        currency_field="capital_currency_id",
        help="Publicly registered capital amount.",
    )
    capital_currency_id = fields.Many2one(
        comodel_name="res.currency", string="Capital currency"
    )
    turnover_range_id = fields.Many2one(
        comodel_name="res.partner.turnover_range", string="Turnover range"
    )
    turnover_amount = fields.Float()
    company_size = fields.Selection(
        string="Company size",
        selection=[
            ("micro", "Micro"),
            ("small", "Small"),
            ("medium", "Medium"),
            ("big", "Big"),
        ],
    )
