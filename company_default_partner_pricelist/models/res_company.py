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

    def _update_partner_pricelist_generic_property(self):
        self.ensure_one()
        default_property_pp = self.default_property_product_pricelist
        ir_property = self.env["ir.property"]
        field = self.env["ir.model.fields"]._get(
            "res.partner", "property_product_pricelist"
        )
        ppty = ir_property.sudo().search(
            [
                ("name", "=", "property_product_pricelist"),
                ("company_id", "=", self.id),
                ("fields_id", "=", field.id),
                ("res_id", "=", False),
            ],
            limit=1,
        )
        if ppty:
            if not default_property_pp:
                ppty.sudo().unlink()
            else:
                ppty.sudo().write(
                    {"value_reference": "product.pricelist,%s" % default_property_pp.id}
                )
        elif default_property_pp:
            ir_property.sudo().create(
                {
                    "name": "property_product_pricelist",
                    "value_reference": "product.pricelist,%s" % default_property_pp.id,
                    "fields_id": field.id,
                    "company_id": self.id,
                }
            )

    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        if "default_property_product_pricelist" in vals:
            res._update_partner_pricelist_generic_property()
        return res

    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if "default_property_product_pricelist" in vals:
            for rec in self:
                rec._update_partner_pricelist_generic_property()
        return res
