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
