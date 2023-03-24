from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_order_ids = fields.Many2many(
        "stock.picking", compute="_compute_delivery_count"
    )
    partner_delivery_count = fields.Integer(compute="_compute_delivery_count")

    @api.model
    def _domain_for_pickings_search(self, partner):
        return [
            ("partner_id", "=", partner.id),
            ("picking_type_id.code", "=", "outgoing"),
        ]

    @api.model
    def _get_partner_pickings(self, partner):
        domain = self._domain_for_pickings_search(partner)
        return self.env["stock.picking"].search(domain)

    def _compute_delivery_count(self):
        for partner in self:
            partner.delivery_order_ids = self._get_partner_pickings(partner)
            partner.partner_delivery_count = len(self._get_partner_pickings(partner))

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
