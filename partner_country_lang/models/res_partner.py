# Copyright 2022-2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Add the compute method on the existing field
    lang = fields.Selection(compute="_compute_lang", store=True, readonly=False)

    @api.depends("country_id")
    def _compute_lang(self):
        if hasattr(super(), "_compute_lang"):
            res = super()._compute_lang()
        for item in self:
            if item.country_id.lang:
                item.lang = item.country_id.lang
        if hasattr(super(), "_compute_lang"):
            return res

    @api.model_create_multi
    def create(self, vals_list):
        """Add lang if the partner is created with a country through code
        and no language is specified.
        """
        for vals in vals_list:
            if vals.get("country_id") and "lang" not in vals:
                country = self.env["res.country"].browse(vals["country_id"])
                if country.lang:
                    vals["lang"] = country.lang
        return super().create(vals_list)
