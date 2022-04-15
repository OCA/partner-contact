# Copyright 2021 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(
        search="_search_property_product_pricelist"
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Substitute pricelist tuple
        partner_domain = [
            (1, "=", 1)
            if (isinstance(x, (list, tuple)) and x[0] == "property_product_pricelist")
            else x
            for x in args
        ]
        return super(
            ResPartner, self.with_context(search_partner_domain=partner_domain)
        ).search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )

    @api.model
    def _search_property_product_pricelist(self, operator, value):
        domain = self.env.context.get("search_partner_domain", [])
        partners = self.with_context(prefetch_fields=False).search(domain)
        key = "property_product_pricelist"
        return [("id", "in", partners.filtered_domain([(key, operator, value)]).ids)]
