# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Convert field to a computed
    picking_policy = fields.Selection(
        compute="_compute_picking_policy", store=True, readonly=False
    )

    @api.depends("partner_id")
    def _compute_picking_policy(self):
        for this in self:
            picking_policy = (
                this.partner_shipping_id.picking_policy
                or this.partner_id.picking_policy
                or self.default_get(["picking_policy"]).get("picking_policy")
            )
            this.picking_policy = picking_policy
