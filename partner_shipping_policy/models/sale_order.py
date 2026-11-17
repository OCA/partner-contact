# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Convert field to a computed
    picking_policy = fields.Selection(
        compute="_compute_picking_policy", store=True, readonly=False, precompute=True
    )

    @api.model
    def default_get(self, fields):
        # A default ends up in the create values and would prevent the compute
        # from applying the partner's policy. It comes from either:
        # - the field default="direct" in sale_stock:
        # https://github.com/odoo/odoo/blob/4fd1a2ea4f90da0a641ce64e12e077cab6c3d851/addons/sale_stock/models/sale_order.py#L21-L24
        # - the Settings option, saved as an ir.default:
        # https://github.com/odoo/odoo/blob/4fd1a2ea4f90da0a641ce64e12e077cab6c3d851/addons/sale_stock/models/res_config_settings.py#L15-L18
        # Only a default explicitly given in the context is kept, or all of
        # them with ``clear_picking_policy_default=False``.
        res = super().default_get(fields)
        if (
            self.env.context.get("clear_picking_policy_default", True)
            and "default_picking_policy" not in self.env.context
        ):
            res.pop("picking_policy", None)
        return res

    def _depends_picking_policy(self):
        depends = []
        if hasattr(super(), "_depends_picking_policy"):
            depends = super()._depends_picking_policy()
        depends += ["partner_shipping_id", "partner_id"]
        return depends

    @api.depends(lambda self: self._depends_picking_policy())
    def _compute_picking_policy(self):
        # Other modules (e.g. sale_order_type) may also compute this field:
        # only override their result with the partner's policy, and fall back
        # on the default when nothing set a value.
        res = None
        if hasattr(super(), "_compute_picking_policy"):
            res = super()._compute_picking_policy()
        default_policy = (
            self.with_context(clear_picking_policy_default=False)
            .default_get(["picking_policy"])
            .get("picking_policy")
        )
        for order in self:
            partner_policy = (
                order.partner_shipping_id.picking_policy
                or order.partner_id.picking_policy
            )
            if partner_policy:
                order.picking_policy = partner_policy
            elif not order.picking_policy:
                order.picking_policy = default_policy
        return res
