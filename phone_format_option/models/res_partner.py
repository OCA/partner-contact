# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # The two onchange methods below override the standard ones from
    # phone_validation, which format the number in international format.
    @api.onchange("phone", "country_id", "company_id")
    def _onchange_phone_validation(self):
        self._format_phone_number_field("phone")

    @api.onchange("mobile", "country_id", "company_id")
    def _onchange_mobile_validation(self):
        self._format_phone_number_field("mobile")

    def _format_phone_number_field(self, fname):
        """Reformat ``fname`` using the configured format. The actual
        formatting is delegated to ``phone_validation``'s ``_phone_format``;
        this module only decides which ``force_format`` to apply."""
        if not self[fname]:
            return
        force_format = self._get_phone_force_format()
        if force_format == "RAW":
            return
        self[fname] = (
            self._phone_format(fname=fname, force_format=force_format) or self[fname]
        )

    def _get_phone_force_format(self):
        self.ensure_one()
        phone_format = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("phone_format_option.phone_format", "INTERNATIONAL")
        )
        company_country = self.env.company.country_id
        partner_country = self.country_id or company_country
        if phone_format == "NATIONAL" and partner_country != company_country:
            return "INTERNATIONAL"
        return phone_format
