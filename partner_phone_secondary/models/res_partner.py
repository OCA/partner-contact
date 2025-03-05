# Copyright 2020 - Iván Todorovich
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    phone2 = fields.Char("Phone (Secondary)")

    @api.onchange("phone2", "country_id", "company_id")
    def _onchange_phone2_validation(self):
        # This is done in onchange to keep consistent with phone_validation
        # phone and mobile validation
        if self.phone2 and hasattr(self, "_phone_format"):
            self.phone2 = (
                self._phone_format(fname="phone2", force_format="INTERNATIONAL")
                or self.phone2
            )
