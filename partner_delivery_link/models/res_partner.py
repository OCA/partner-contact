from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_order_ids = fields.Many2many(
        "stock.picking", compute="_compute_delivery_count"
    )
    delivery_count = fields.Integer(compute="_compute_delivery_count")

    def _compute_delivery_count(self):
        for partner in self:
            delivery_order_ids = self.env["stock.picking"].search(
                [
                    ("partner_id", "=", self.id),
                    ("picking_type_id.code", "=", "outgoing"),
                ]
            )
            partner.delivery_order_ids = delivery_order_ids
            partner.delivery_count = len(delivery_order_ids)

    def action_view_partner_delivery(self):
        delivery_tree_view = self.env.ref("stock.vpicktree")
        delivery_form_view = self.env.ref("stock.view_picking_form")
        return {
            "name": "Transfers",
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "view_type": "form",
            "view_mode": "tree, form",
            "views": [(delivery_tree_view.id, "tree"), (delivery_form_view.id, "form")],
            "domain": [("id", "in", self.delivery_order_ids.ids)],
        }
