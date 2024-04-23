# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_customer = fields.Boolean(
        compute="_compute_is_customer",
        inverse="_inverse_is_customer",
        store=True,
        readonly=False,
        string="Is a Customer",
    )
    is_supplier = fields.Boolean(
        compute="_compute_is_supplier",
        inverse="_inverse_is_supplier",
        store=True,
        readonly=False,
        string="Is a Supplier",
    )

    @api.depends("customer_rank")
    def _compute_is_customer(self):
        for partner in self:
            partner.is_customer = bool(partner.customer_rank)

    @api.depends("supplier_rank")
    def _compute_is_supplier(self):
        for partner in self:
            partner.is_supplier = bool(partner.supplier_rank)

    def _inverse_is_customer(self):
        self.filtered(lambda p: not p.is_customer).write({"customer_rank": 0})
        self.filtered(lambda p: p.is_customer and not p.customer_rank).write(
            {"customer_rank": 1}
        )

    def _inverse_is_supplier(self):
        self.filtered(lambda p: not p.is_supplier).write({"supplier_rank": 0})
        self.filtered(lambda p: p.is_supplier and not p.supplier_rank).write(
            {"supplier_rank": 1}
        )

    def _increase_rank(self, field):
        super()._increase_rank(field)
        if self.ids and field in ["customer_rank", "supplier_rank"]:
            self.modified([field])
