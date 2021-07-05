from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_email_check_filter_duplicates = fields.Boolean(
        related="company_id.partner_email_check_filter_duplicates", readonly=False,
    )

    partner_email_check_check_deliverability = fields.Boolean(
        related="company_id.partner_email_check_check_deliverability", readonly=False,
    )
