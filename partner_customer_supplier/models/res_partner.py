from odoo import _, api, fields, models
from odoo.exceptions import UserError

DOMAIN_SEARCH = {
    ("=", False): ("=", 0),
    ("=", True): (">=", 1),
    ("!=", False): (">=", 1),
    ("!=", True): ("=", 0),
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer = fields.Boolean(
        string="Is Customer",
        compute="_compute_partner_is_customer",
        inverse="_inverse_partner_is_customer",
        search="_search_partner_is_customer",
    )
    supplier = fields.Boolean(
        string="Is Vendor",
        compute="_compute_partner_is_supplier",
        inverse="_inverse_partner_is_supplier",
        search="_search_partner_is_supplier",
    )

    @api.depends("customer_rank")
    def _compute_partner_is_customer(self):
        for partner in self:
            partner.customer = partner.customer_rank > 0

    def _inverse_partner_is_customer(self):
        self.filtered(lambda p: not p.customer).write({"customer_rank": 0})
        self.filtered(lambda p: p.customer and not p.customer_rank).write(
            {"customer_rank": 1}
        )

    def _search_partner_is_customer(self, operator, value):
        if operator not in ["=", "!="] or not isinstance(value, bool):
            raise UserError(_("Operation not supported"))
        operator, value = DOMAIN_SEARCH.get((operator, value))
        return [("customer_rank", operator, value)]

    @api.depends("supplier_rank")
    def _compute_partner_is_supplier(self):
        for partner in self:
            partner.supplier = partner.supplier_rank > 0

    def _inverse_partner_is_supplier(self):
        self.filtered(lambda p: not p.supplier).write({"supplier_rank": 0})
        self.filtered(lambda p: p.supplier and not p.supplier_rank).write(
            {"supplier_rank": 1}
        )

    def _search_partner_is_supplier(self, operator, value):
        if operator not in ["=", "!="] or not isinstance(value, bool):
            raise UserError(_("Operation not supported"))
        operator, value = DOMAIN_SEARCH.get((operator, value))
        return [("supplier_rank", operator, value)]
