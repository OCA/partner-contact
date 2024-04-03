# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    picking_policy = fields.Selection(
        selection="_get_picking_policy_selection",
        string="Shipping Policy",
        help="Shipping policy to use in this partner's sales orders. If you deliver all "
        "products at once, the delivery order will be scheduled based on the greatest "
        "product lead time. Otherwise, it will be based on the shortest.",
    )

    @api.model
    def _get_picking_policy_selection(self):
        return self.env["sale.order"].fields_get(["picking_policy"])["picking_policy"][
            "selection"
        ]
