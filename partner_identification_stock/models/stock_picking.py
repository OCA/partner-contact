from odoo import _, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_id_requirement(self):
        for rec in self:
            rec.require_partner_identification = (
                rec.valid_partner_identification
            ) = False
            for line in rec.move_lines:
                if line.product_id.require_id_stock_ids:
                    rec.require_partner_identification = True
                ffl_lines = rec.partner_id.id_numbers.filtered(
                    lambda i: i.category_id.id
                    in line.product_id.require_id_stock_ids.ids
                    and i.valid_until
                )
                if any(
                    line.valid_until >= fields.Date.today()
                    and line.status in ["open", "pending"]
                    for line in ffl_lines
                ):
                    rec.valid_partner_identification = True

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
