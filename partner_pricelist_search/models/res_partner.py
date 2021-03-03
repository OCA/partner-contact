# Copyright 2021 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Pricelist(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(
        search="_search_property_product_pricelist"
    )

    @api.model
    def _search_property_product_pricelist(self, operator, value):
        if operator == "=":

            def filter_func(partner):
                return partner.property_product_pricelist.id == value

        elif operator == "!=":

            def filter_func(partner):
                return partner.property_product_pricelist.id != value

        elif operator == "in":

            def filter_func(partner):
                return partner.property_product_pricelist.id in value

        elif operator == "not in":

            def filter_func(partner):
                return partner.property_product_pricelist.id not in value

        else:
            raise UserError(
                _("Pricelist field do not support search with the operator '%s'.")
                % operator
            )
        partners = self.with_context(prefetch_fields=False).search([])
        return [("id", "in", partners.filtered(filter_func).ids)]
