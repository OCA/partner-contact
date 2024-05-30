# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, models
from odoo.exceptions import AccessError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        """Simulate that you do not have ACLs so that the create, edit and delete
        buttons are not displayed."""
        user = self.env.user
        group = "partner_readonly_security.group_partner_edition"
        test_condition = not config["test_enable"] or (
            config["test_enable"]
            and self.env.context.get("test_partner_readonly_security")
        )
        if (
            test_condition
            and operation != "read"
            and not self.env.su
            and not user.has_group(group)
        ):
            if raise_exception:
                raise AccessError(
                    _(
                        "Sorry, you are not allowed to create/edit partners. Please "
                        "contact your administrator for further information."
                    )
                )
            return False
        return super().check_access_rights(
            operation=operation, raise_exception=raise_exception
        )
