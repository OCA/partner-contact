import logging
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class ResPartner(models.Model):
    """Partner with birth date in date format."""

    _inherit = "res.partner"

    birthdate_date = fields.Date("Birthdate")

    # Scheduler function for birthday mail send
    def birthday_mail_send(self):
        partners = self.env["res.partner"].search(
            [("birthdate_date", "!=", False), ("email", "!=", False)]
        )

        for partner in partners:
            # Get the age of partner
            years = relativedelta(date.today(), partner.birthdate_date).years
            months = relativedelta(date.today(), partner.birthdate_date).months
            days = relativedelta(date.today(), partner.birthdate_date).days
            logging.info("Information+++++++++++++++")
            logging.info(years)
            logging.info(months)
            logging.info(days)
            # Send Birthday wish if today is his birthday
            if months == 0 and days == 0:
                logging.info("Send wish+++++++++")
                template_id = self.env.ref(
                    "partner_contact_birthdate.mail_template_birthday_wish"
                ).id  # Get mail template
                template = self.env["mail.template"].browse(template_id)
                template.write(
                    {"email_to": partner.email}
                )  # Write the email address of partner
                template.send_mail(self.id, force_send=True)
