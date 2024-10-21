from odoo import _, api, models


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.onchange("value")
    def warning_partners_depth_exceeded(self):
        if self.key == "partner_contact_restrict_depth.contacts_max_depth":
            if int(self.value) > 0:
                partners = self.env["res.partner"].partners_with_depth_exceeded(
                    self.value
                )
                if partners:
                    return {
                        "warning": {
                            "title": _("Partners depth exceeded"),
                            "message": "Your system have "
                            + str(len(partners))
                            + " contacts with depth higher than "
                            + str(self.value)
                            + ". Please review those contacts and resolve them.",
                        }
                    }
