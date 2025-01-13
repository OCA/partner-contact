# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user
from odoo.tests.common import users
from odoo.tools import mute_logger


class TestPartnerReadonlySecurity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
                test_partner_readonly_security=True,
            )
        )
        cls.user_admin = new_test_user(
            cls.env,
            login="test_user_admin",
            groups="""
                base.group_user,base.group_partner_manager,
                partner_readonly_security.group_partner_edition
            """,
        )
        cls.user_readonly = new_test_user(
            cls.env,
            login="test_user_readonly",
            groups="base.group_user,base.group_partner_manager",
        )
        cls.partner = cls.env["res.partner"].sudo().create({"name": "Test partner"})

    @users("test_user_admin")
    @mute_logger("odoo.models.unlink")
    def test_partner_admin(self):
        """Read, write, unlink and create allowed."""
        partners = self.env["res.partner"].search([])
        self.assertIn(self.partner, partners)
        self.partner.with_user(self.env.user).write({"name": "new-name"})
        self.partner.with_user(self.env.user).unlink()
        new_partner = self.env["res.partner"].create({"name": "Test partner 2"})
        self.assertTrue(new_partner.exists())

    @users("test_user_readonly")
    def test_partner_readonly(self):
        """Read allowed. Write, unlink and create not allowed."""
        partners = self.env["res.partner"].search([])
        self.assertIn(self.partner, partners)
        with self.assertRaises(AccessError):
            self.partner.with_user(self.env.user).write({"name": "new-name"})
        with self.assertRaises(AccessError):
            self.partner.with_user(self.env.user).unlink()
        with self.assertRaises(AccessError):
            self.env["res.partner"].create({"name": "Test partner 2"})
