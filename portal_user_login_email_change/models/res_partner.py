# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _update_user_login(self, partner, old_email):
        # Check if there is a related user with the same login as the old email
        if partner.user_ids:
            user = partner.user_ids.filtered(lambda u: u.login == old_email)
            if user:
                user.write({"login": partner.email})

    def write(self, vals):
        if "email" not in vals or not self.env.user.has_group("base.group_portal"):
            return super().write(vals)
        # Capture the old email for each partner before the update
        old_emails = {partner.id: partner.email for partner in self}
        result = super().write(vals)
        # Update user login if email has changed
        for partner in self:
            old_email = old_emails.get(partner.id)
            new_email = vals.get("email")
            if old_email != new_email:
                self._update_user_login(partner, old_email)
        return result
