# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange("mobile", "country_id", "company_id")
    def _onchange_mobile_validation(self):
        if self.mobile:
            self.mobile = (
                self._phone_format(fname="mobile", force_format="INTERNATIONAL")
                or self.mobile
            )

    # no need to inherit the method _phone_get_number_fields() because by default
    # it has 'phone' and 'mobile' if the 2 fields exist on self
