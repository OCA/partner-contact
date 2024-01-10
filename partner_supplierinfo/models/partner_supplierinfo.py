# Copyright 2022 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PartnerSupplierInfo(models.Model):
    _name = "partner.supplierinfo"
    _description = "Partner reference equivalence to identify another partner"

    ref = fields.Char()
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    supplier_id = fields.Many2one(comodel_name="res.partner", required=True)

    _sql_constraints = [
        (
            "unique_ref",
            "unique (supplier_id, partner_id)",
            "A reference of this supplier already exists.",
        )
    ]
