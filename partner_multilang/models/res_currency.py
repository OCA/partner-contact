# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Currency(models.Model):
    _inherit = "res.currency"

    symbol = fields.Char(translate=True)
    currency_unit_label = fields.Char(translate=True)
    currency_subunit_label = fields.Char(translate=True)
