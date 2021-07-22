from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    require_id_sale_ids = fields.Many2many(
        "res.partner.id_category",
        "product_category_res_partner_id_category_rel" "product_category_id",
        "res_partner_id_category",
        string="Require ID for Sales Orders",
    )
