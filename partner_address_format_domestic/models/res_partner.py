# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_address_format(self):
        country = self.country_id
        if country == self.env.company.country_id and country.address_format_domestic:
            return country.address_format_domestic
        return super()._get_address_format()
