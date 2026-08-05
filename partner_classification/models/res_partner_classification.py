# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerClassification(models.Model):
    _name = "res.partner.classification"
    _description = "Partner Classification"
    _order = "name"

    name = fields.Char(required=True, translate=True)

    code = fields.Char()

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        "res.company",
        index=True,
    )

    _unique_code = models.Constraint(
        "UNIQUE(code)",
        "This code is already taken",
    )
