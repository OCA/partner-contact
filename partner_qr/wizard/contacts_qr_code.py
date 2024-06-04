import base64
from io import BytesIO

import qrcode

from odoo import api, fields, models


class ContactsQRCode(models.TransientModel):
    """This model is used to show the QR Code of the Contact."""

    _name = "contacts.qr.code"
    _description = "QR Code Wizard"

    qr_code = fields.Image(string="", compute="_compute_qr_code", store=True)

    fullname = fields.Boolean(string="Full Name", default="True")  # FN
    company_name = fields.Boolean(default="True")  # ORG
    job_title = fields.Boolean(default="True")  # TITLE
    email = fields.Boolean(default="True")  # EMAIL
    url = fields.Boolean(string="Company URL", default="True")  # URL

    @api.depends("fullname", "company_name", "job_title", "email", "url")
    def _compute_qr_code(self):
        """
        Called everytime the user clicks on any check field.
        It is used to change the QR Code to contain only the
        relevant information the user wants to export

        :return: None
        """
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if active_model and active_id:
            record = self.env[active_model].browse(active_id)
        else:
            return

        # Prepared VCARD structure according to the phone's format
        vcard = f"BEGIN:VCARD\nTEL:{record.phone}\n"
        if self.fullname and record.name:
            vcard += f"FN:{record.name}\n"
        if self.company_name and record.parent_id.name:
            vcard += f"ORG:{record.parent_id.name}\n"
        if self.job_title and record.function:
            vcard += f"TITLE:{record.function}\n"
        if self.email and record.email:
            vcard += f"EMAIL;TYPE=WORK:{record.email}\n"
        if self.url and record.website:
            vcard += f"URL:{record.website}\n"
        vcard += "END:VCARD"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(vcard)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        self.qr_code = img_str

    def download_qr(self):
        """
        Called when the user clicks on the "Download this QR Code button".
        It starts a download for the selected QR Code.
        :return: dict[str, str | LiteralString] (download link)
        """
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if active_model and active_id:
            record = self.env[active_model].browse(active_id)
        else:
            return

        # Get base url
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        attachment_obj = self.env["ir.attachment"]
        # Create attachment
        attachment_id = attachment_obj.create(
            {"name": record.name + "'s QR Code", "datas": self.qr_code}
        )
        # Prepare download url
        download_url = "/web/content/" + str(attachment_id.id) + "?download=true"
        # Download
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "form",
        }
