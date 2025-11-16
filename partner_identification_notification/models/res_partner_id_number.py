from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    notification_date = fields.Date(copy=False)

    def write(self, vals):
        # A renewed ID (new expiry date) must be notified again; rewriting
        # the same date (imports, automations) must not re-arm it
        renewed = self.browse()
        if "valid_until" in vals and "notification_date" not in vals:
            valid_until = fields.Date.to_date(vals["valid_until"])
            renewed = self.filtered(
                lambda r: r.notification_date and r.valid_until != valid_until
            )
        res = super().write(vals)
        if renewed:
            renewed.write({"notification_date": False})
        return res

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
