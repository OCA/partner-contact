# Copyright 2022 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    supplier_info_ids = fields.One2many(
        comodel_name="partner.supplierinfo", inverse_name="partner_id"
    )
    supplier_ref = fields.Char(compute="_compute_ref")

    @api.depends_context("supplier_id")
    def _compute_ref(self):
        for partner in self:
            partner.supplier_ref = (
                partner.supplier_info_ids.filtered(
                    lambda x: x.supplier_id.id == self.env.context.get("supplier_id")
                ).ref
                or partner.ref
            )
