# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_partner_pricelist_multi_search_domain_hook(self, company_id):
        res = super()._get_partner_pricelist_multi_search_domain_hook(company_id)
        company = self.env["res.company"].browse(company_id)
        if company and company.default_property_product_pricelist:
            res.append(("id", "=", company.default_property_product_pricelist.id))
        return res
