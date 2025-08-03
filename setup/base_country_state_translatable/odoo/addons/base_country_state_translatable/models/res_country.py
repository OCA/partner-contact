# Copyright 2017 initOS GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CountryState(models.Model):
    _inherit = "res.country.state"

    name = fields.Char(translate=True)
