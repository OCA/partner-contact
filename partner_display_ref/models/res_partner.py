# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("ref")
    @api.depends_context("partner_display_ref_field")
    def _compute_display_name(self):
        super()._compute_display_name()
        ctx = self.env.context
        field_name = ctx.get("partner_display_ref_field")
        if not field_name:
            return
        if field_name not in self._fields:
            return
        for partner in self:
            value = partner[field_name]
            if value:
                partner.display_name = f"[{value}] {partner.display_name}"
