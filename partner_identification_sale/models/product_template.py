from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_id_sale_ids = fields.Many2many(
        "res.partner.id_category",
        "product_template_res_partner_id_category_sale_rel",
        "product_template_id",
        "res_partner_id_category_id",
        string="Require ID for Sales Orders",
    )

    @api.onchange("categ_id")
    def _onchange_categ_id_require_id_sale_ids(self):
        self.require_id_sale_ids = [(6, 0, self.categ_id.require_id_sale_ids.ids)]
