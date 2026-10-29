from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    def _get_default_id_number_model(self):
        return self.env.ref("partner_identification.model_res_partner_id_number").id

    send_notification = fields.Boolean()
    days_before_expire = fields.Integer(
        string="# of Days Before Expiration",
    )
    email_template_id = fields.Many2one(
        "mail.template",
        domain=[("model", "=", "res.partner.id_number")],
    )
    id_number_model_id = fields.Many2one(
        "ir.model", default=lambda self: self._get_default_id_number_model()
    )

    @api.constrains("email_template_id")
    def _check_email_template_model(self):
        for rec in self:
            template = rec.email_template_id
            if template and template.model != "res.partner.id_number":
                raise ValidationError(
                    self.env._(
                        "The email template of ID category %(category)s must be "
                        "defined on the Partner ID Number model.",
                        category=rec.name,
                    )
                )
