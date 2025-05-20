# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange("country_id")
    def _onchange_country_id(self):
        super()._onchange_country_id()
        if self.country_id.lang:
            self.lang = self.country_id.lang

    def _adjust_lang_by_country(self, vals):
        """Adjust vals dictionary for adding the language of the country
        if no one is included in it, but country is.
        """
        if vals.get("country_id") and "lang" not in vals:
            country = self.env["res.country"].browse(vals["country_id"])
            if country.lang:
                vals["lang"] = country.lang

    @api.model_create_multi
    def create(self, vals_list):
        """Add lang if the partner is created with a country through code
        and no language is specified.
        """
        for vals in vals_list:
            self._adjust_lang_by_country(vals)
        return super().create(vals_list)

    def write(self, vals):
        """Change language if a country is written through code and no
        one is modified as well.
        """
        self._adjust_lang_by_country(vals)
        return super().write(vals)
