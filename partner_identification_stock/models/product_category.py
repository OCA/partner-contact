from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    require_id_stock_ids = fields.Many2many(
        "res.partner.id_category",
        string="Require ID for Delivery Orders",
    )
