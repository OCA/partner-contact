# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    phone2 = fields.Char("Phone (Secondary)")
    # Companion fields read by the phone widget (see phone_validation):
    # phone2 keeps the raw input, display/dial use these.
    phone2_sanitized = fields.Char(
        compute="_compute_phone2_companion_fields", export_string_translation=False
    )
    phone2_formatted = fields.Char(
        compute="_compute_phone2_companion_fields", export_string_translation=False
    )

    @api.depends("phone2", "country_id", "company_id")
    def _compute_phone2_companion_fields(self):
        if hasattr(self, "_phone_update_companion_fields"):
            self._phone_update_companion_fields(["phone2"])
        else:
            # phone_validation not installed: widget falls back to raw phone2
            self.phone2_sanitized = False
            self.phone2_formatted = False
