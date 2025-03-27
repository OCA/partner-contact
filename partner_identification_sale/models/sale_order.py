from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_id_requirement(self):
        for rec in self:
            rec.require_id = rec.valid_id = False
            if rec.state == "sale":
                continue
            require_id_sale_ids = set(
                rec.order_line.product_id.mapped("require_id_sale_ids").ids
            )
            if require_id_sale_ids:
                rec.require_id = True
                ffl_lines = [
                    i
                    for i in rec.partner_id.id_numbers
                    if i.category_id.id in require_id_sale_ids and i.valid_until
                ]
                today = fields.Date.today()
                rec.valid_id = any(
                    line.valid_until >= today and line.status in ["open", "pending"]
                    for line in ffl_lines
                )

    require_id = fields.Boolean(string="Require ID?", compute="_compute_id_requirement")
    valid_id = fields.Boolean(string="Valid ID?", compute="_compute_id_requirement")

    def action_confirm(self):
        for rec in self:
            if rec.require_id and not rec.valid_id:
                raise UserError(
                    _(
                        "Cannot confirm a Sales Order without an active license."
                        " Please resolve the license issue then try again."
                    )
                )

        return super().action_confirm()
