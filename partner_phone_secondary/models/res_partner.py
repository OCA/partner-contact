# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    phone2 = fields.Char("Phone (Secondary)")

    @api.onchange("phone2", "country_id", "company_id")
    def _onchange_phone2_validation(self):
        # Compatibility with phone_validation
        if hasattr(self, "phone_format"):
            if self.phone2:
                self.phone2 = self.phone_format(self.phone2)
