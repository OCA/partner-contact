# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_rank_auto = fields.Boolean(
        string="Automatic Partner Rank Management",
        config_parameter="partner_manual_rank.partner_rank_auto",
    )
