# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Convert field to a computed
    picking_policy = fields.Selection(
        compute="_compute_picking_policy", store=True, readonly=False
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if "picking_policy" in fields_list:
            if "default_picking_policy" not in self.env.context:
                partner_id = self.env.context.get(
                    "default_partner_id"
                ) or self.env.context.get("active_id")
                if partner_id:
                    partner = self.env["res.partner"].browse(partner_id)
                    partner_policy = (
                        partner.commercial_partner_id.picking_policy
                        or partner.picking_policy
                    )
                    if partner_policy:
                        res["picking_policy"] = partner_policy
        return res

    @api.depends("partner_id")
    def _compute_picking_policy(self):
        for this in self:
            picking_policy = (
                this.partner_shipping_id.picking_policy
                or this.partner_id.picking_policy
                or self.default_get(["picking_policy"]).get("picking_policy")
            )
            this.picking_policy = picking_policy
