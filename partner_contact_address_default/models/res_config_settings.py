# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contact_address_default_allow_all_partners = fields.Boolean(
        related="company_id.contact_address_default_allow_all_partners",
        readonly=False,
    )
