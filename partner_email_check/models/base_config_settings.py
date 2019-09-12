from odoo import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    partner_email_check_filter_duplicates = fields.Boolean(
        string="Filter duplicate partner email addresses",
        help="Don't allow multiple partners to have the same email address.",
    )

    partner_email_check_check_deliverability = fields.Boolean(
        string="Check deliverability of email addresses",
        help="Don't allow email addresses with providers that don't exist",
    )

    @api.multi
    def set_partner_email_check_filter_duplicates(self):
        self.env['ir.config_parameter'].set_param(
            'partner_email_check_filter_duplicates',
            str(self.partner_email_check_filter_duplicates)
        )

    @api.model
    def get_default_partner_email_check_filter_duplicates(self, fields):
        return {
            'partner_email_check_filter_duplicates':
                self.env['ir.config_parameter'].get_param(
                    'partner_email_check_filter_duplicates', 'False'
                ) == 'True'
        }

    @api.multi
    def set_partner_email_check_check_deliverability(self):
        self.env['ir.config_parameter'].set_param(
            'partner_email_check_check_deliverability',
            str(self.partner_email_check_check_deliverability)
        )

    @api.model
    def get_default_partner_email_check_check_deliverability(self, fields):
        return {
            'partner_email_check_check_deliverability':
                self.env['ir.config_parameter'].get_param(
                    'partner_email_check_check_deliverability', 'False'
                ) == 'True'
        }
