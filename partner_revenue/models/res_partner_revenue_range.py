# Copyright 2026 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerRevenueRange(models.Model):
    _name = "res.partner.revenue_range"
    _description = "Revenue range"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique!"),
    ]

    name = fields.Char(required=True, translate=True)
