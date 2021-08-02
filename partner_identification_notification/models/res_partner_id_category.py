from odoo import fields, models


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    def _get_default_id_number_model(self):
        return self.env.ref("partner_identification.model_res_partner_id_number").id

    send_notification = fields.Boolean(
        string="Send Notification",
    )
    days_before_expire = fields.Integer(
        string="# of Days Before Expiration",
    )
    email_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
    )
    id_number_model_id = fields.Many2one(
        "ir.model", default=_get_default_id_number_model
    )
