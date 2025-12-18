# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_address_details = fields.Text(translate=True)

    def _prepare_display_address(self, without_company=False):
        self.ensure_one()
        address_format, args = super()._prepare_display_address(
            without_company=without_company
        )
        if self.partner_address_details and self.env.context.get("is_report"):
            address_format = self.partner_address_details
        return address_format, args
