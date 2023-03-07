# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    restrict_filter_id = fields.Many2one(
        "ir.filters",
        ondelete="cascade",
        domain=[("model_id", "=", "res.partner")],
        context={"default_model_id": "res.partner"},
    )
