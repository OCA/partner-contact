from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    partner_email_check_filter_duplicates = fields.Boolean(
        string="Filter duplicate partner email addresses",
        help="Don't allow multiple partners to have the same email address.",
    )

    partner_email_check_check_deliverability = fields.Boolean(
        string="Check deliverability of email addresses",
        help="Don't allow email addresses with providers that don't exist",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        conf = self.env['ir.config_parameter'].sudo()
        res.update(
            partner_email_check_filter_duplicates=conf.get_param(
                'partner_email_check_filter_duplicates', 'False'
            ) == 'True',
            partner_email_check_check_deliverability=conf.get_param(
                'partner_email_check_check_deliverability', 'False'
            ) == 'True',
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        conf = self.env['ir.config_parameter'].sudo()
        conf.set_param(
            'partner_email_check_filter_duplicates',
            self.partner_email_check_filter_duplicates
        )
        conf.set_param(
            'partner_email_check_check_deliverability',
            self.partner_email_check_check_deliverability
        )
