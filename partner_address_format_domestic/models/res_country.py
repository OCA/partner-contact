# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    address_format_domestic = fields.Text(string="Domestic Address Format")
    is_relevant_for_company = fields.Boolean(compute="_compute_is_relevant_for_company")

    def _compute_is_relevant_for_company(self):
        company_countries = self.env["res.company"].search([]).mapped("country_id.id")
        for country in self:
            country.is_relevant_for_company = country.id in company_countries
