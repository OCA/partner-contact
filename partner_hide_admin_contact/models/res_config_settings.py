# Copyright 2026 Canarias Conectada
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_hide_admin_contact = fields.Boolean(
        string="Hide administrator contacts",
        help="Hide any system administrator's contact from regular "
        "internal users, in Contacts. Administrators keep seeing every "
        "contact, including other administrators. Disable if this breaks "
        "a legitimate use case, such as adding an administrator as a "
        "follower.",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        rule = self.env.ref(
            "partner_hide_admin_contact.res_partner_rule_hide_admin_contact",
            raise_if_not_found=False,
        )
        res["partner_hide_admin_contact"] = bool(rule and rule.active)
        return res

    def set_values(self):
        result = super().set_values()
        rule = self.env.ref(
            "partner_hide_admin_contact.res_partner_rule_hide_admin_contact",
            raise_if_not_found=False,
        )
        if rule:
            rule.sudo().active = self.partner_hide_admin_contact
        return result
