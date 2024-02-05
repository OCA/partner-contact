from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_partner_and_price(self):
        partner_id = self.env.context.get("partner_id")
        partner = self.env["res.partner"].browse(partner_id)
        pricelist = None
        if partner:
            pricelist = partner.property_product_pricelist

        for product in self:
            product.partner_id = partner_id
            product.partner_price = product.lst_price
            if pricelist:
                product.partner_price = pricelist._get_product_price(
                    product, quantity=1
                )

    partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        compute="_compute_partner_and_price",
    )
    partner_price = fields.Float(
        "Contact's Price",
        compute="_compute_partner_and_price",
        digits=2,
    )
