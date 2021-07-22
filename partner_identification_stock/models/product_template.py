from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_id_stock_ids = fields.Many2many(
        "res.partner.id_category", string="Require ID for Delivery Orders"
    )

    @api.onchange("categ_id")
    def _onchange_categ_id_require_id_stock_ids(self):
        self.require_id_stock_ids = [(6, 0, self.categ_id.require_id_stock_ids.ids)]
