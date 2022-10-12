from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_mobile_unique_filter_duplicates = fields.Boolean(
        related="company_id.partner_mobile_unique_filter_duplicates",
        readonly=False,
    )
