from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _name = "res.partner.id_number"
    _inherit = ["res.partner.id_number", "mail.thread", "mail.activity.mixin"]

    notification_date = fields.Date(string="Notification Date")

    @api.model
    def send_notification(self):
        today = fields.date.today()
        rec_ids = self.search(
            [
                ("category_id.send_notification", "=", True),
                ("category_id.days_before_expire", ">", 0),
                ("status", "in", ["open", "pending"]),
            ]
        )
        for rec in rec_ids:
            days_before_expire = rec.category_id.days_before_expire
            date_from = today - relativedelta(days=days_before_expire)
            if (
                rec.valid_until
                and days_before_expire
                and rec.valid_until >= date_from
                and rec.valid_until <= today
                and rec.category_id.email_template_id
                and not rec.notification_date
            ):
                rec.notification_date = today
                rec.category_id.email_template_id.send_mail(
                    rec.id,
                    force_send=True,
                )
