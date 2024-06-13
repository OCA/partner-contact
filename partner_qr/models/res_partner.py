from odoo import models
from odoo.tools.translate import _


class ResPartner(models.Model):
    _inherit = "res.partner"

    def generate_qr_code_wizard(self):
        """
        Called when the user clicks the
        button on a partner's action's list. It opens a
        new wizard to compose and show a QR Code with their information.

        :return: dict[str, str | dict[str, Any]] (wizard initialization dict)
        """
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("%s's Contact QR Code") % self.name,
            "res_model": "contacts.qr.code",
            "target": "new",
            "view_mode": "form",
            "view_type": "form",
            "context": {"default_contact": self.id},
        }
