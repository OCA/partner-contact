from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    notification_date = fields.Date(copy=False)

    def write(self, vals):
        # A renewed ID (new expiry date) must be notified again
        if "valid_until" in vals and "notification_date" not in vals:
            vals = dict(vals, notification_date=False)
        return super().write(vals)

    @api.model
    def send_notification(self):
        today = fields.Date.today()
        rec_ids = self.search(
            [
                ("category_id.send_notification", "=", True),
                ("category_id.days_before_expire", ">", 0),
                ("category_id.email_template_id", "!=", False),
                ("status", "in", ["open", "pending"]),
                ("valid_until", ">=", today),
                ("notification_date", "=", False),
            ]
        )
        for rec in rec_ids:
            days_before_expire = rec.category_id.days_before_expire
            if rec.valid_until <= today + relativedelta(days=days_before_expire):
                rec.notification_date = today
                rec.category_id.email_template_id.send_mail(
                    rec.id,
                    force_send=True,
                )
