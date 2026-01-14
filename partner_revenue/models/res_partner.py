# Copyright 2026 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    revenue_range_id = fields.Many2one(
        comodel_name="res.partner.revenue_range", string="Revenue range"
    )
