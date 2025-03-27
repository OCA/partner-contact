from odoo import _, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_id_requirement(self):
        for rec in self:
            rec.valid_partner_identification = False
            required_stock_ids = [
                sid
                for line in rec.move_ids
                for sid in line.product_id.require_id_stock_ids.ids
            ]
            rec.require_partner_identification = bool(required_stock_ids)
            if rec.partner_id.id_numbers:
                rec.valid_partner_identification = any(
                    id_num.valid_until
                    and id_num.valid_until >= fields.Date.today()
                    and id_num.status in ["open", "pending"]
                    for id_num in rec.partner_id.id_numbers
                    if id_num.category_id.id in required_stock_ids
                )

    require_partner_identification = fields.Boolean(
        string="Require ID?", compute="_compute_id_requirement"
    )
    valid_partner_identification = fields.Boolean(
        string="Valid ID?", compute="_compute_id_requirement"
    )

    def action_confirm(self):
        for rec in self:
            if (
                rec.require_partner_identification
                and rec.state not in ["draft", "close"]
                and not rec.valid_partner_identification
            ):
                raise UserError(
                    _(
                        "Cannot confirm a Sales Order without valid "
                        "partner identification."
                        " Please resolve the license issue then try again."
                    )
                )

        return super().action_confirm()
