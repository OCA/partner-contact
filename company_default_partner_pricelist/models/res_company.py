# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    default_property_product_pricelist = fields.Many2one(
        "product.pricelist",
        string="Default Account Pricelist",
        help="Default pricelist for this company for new partners.",
    )

    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        if res["default_property_product_pricelist"]:
            field = self.env["ir.model.fields"]._get(
                "res.partner", "property_product_pricelist"
            )
            IrProperty = self.env["ir.property"].sudo()
            ppty = IrProperty.search(
                [
                    ("fields_id", "=", field.id),
                    ("company_id", "=", res.id),
                    ("res_id", "=", False),
                ],
                limit=1,
            )
            values = {
                "value_reference": "product.pricelist,%s"
                % res["default_property_product_pricelist"].id,
            }
            ppty.write(values)
        return res

    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if "default_property_product_pricelist" in vals:
            field = self.env["ir.model.fields"]._get(
                "res.partner", "property_product_pricelist"
            )
            IrProperty = self.env["ir.property"].sudo()
            ppty = IrProperty.search(
                [
                    ("fields_id", "=", field.id),
                    ("company_id", "=", self.id),
                    ("res_id", "=", False),
                ],
                limit=1,
            )
            if ppty:
                values = {
                    "value_reference": "product.pricelist,%s"
                    % vals["default_property_product_pricelist"],
                }
                ppty.write(values)
        return res
