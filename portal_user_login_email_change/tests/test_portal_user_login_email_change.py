# Copyright 2024 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestPortalUserLoginEmailChange(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_partner = cls.env["res.partner"].create(
            {
                "name": "Portal Test Partner",
                "email": "portalpartner@example.com",
            }
        )
        cls.portal_user = (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "Portal Test User",
                    "login": "portalpartner@example.com",
                    "partner_id": cls.portal_partner.id,
                    "groups_id": [Command.set([cls.env.ref("base.group_portal").id])],
                }
            )
        )

    def test_portal_user_login_email_change(self):
        self.portal_partner.with_user(self.portal_user).sudo().write(
            {"email": "test@example.com"}
        )
        self.assertEqual(self.portal_user.login, "test@example.com")
