from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_email_check_syntax = fields.Boolean(
        related="company_id.partner_email_check_syntax",
        readonly=False,
    )

    partner_email_check_filter_duplicates = fields.Boolean(
        related="company_id.partner_email_check_filter_duplicates",
        readonly=False,
    )

    partner_email_check_check_deliverability = fields.Boolean(
        related="company_id.partner_email_check_check_deliverability",
        readonly=False,
    )

    @api.onchange(
        "partner_email_check_syntax", "partner_email_check_check_deliverability"
    )
    def _onchange_partner_email_check_check_deliverability(self):
        if self.partner_email_check_check_deliverability:
            self.partner_email_check_syntax = True
