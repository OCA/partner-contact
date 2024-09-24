# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_block_invoice_address = fields.Boolean(
        config_parameter="partner_block_invoice_address"
    )
    partner_block_invoice_address_default_type = fields.Selection(
        [
            ("contact", "Contact"),
            ("delivery", "Delivery Address"),
            ("other", "Other Address"),
        ],
        default="other",
        config_parameter="partner_block_invoice_address_default_type",
    )
