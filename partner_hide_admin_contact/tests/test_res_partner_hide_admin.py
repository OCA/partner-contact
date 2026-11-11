# Copyright 2026 Canarias Conectada
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPartnerHideAdminContact(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.merchant = new_test_user(
            cls.env, login="hide_admin_merchant", groups="base.group_user"
        )
        cls.colleague = new_test_user(
            cls.env, login="hide_admin_colleague", groups="base.group_user"
        )
        cls.admin = new_test_user(
            cls.env, login="hide_admin_the_admin", groups="base.group_system"
        )

    def test_regular_colleague_is_visible(self):
        self.assertEqual(
            self.colleague.partner_id.with_user(self.merchant).name,
            self.colleague.partner_id.sudo().name,
        )

    def test_admin_contact_is_hidden(self):
        with self.assertRaises(AccessError):
            self.admin.partner_id.with_user(self.merchant).name  # noqa: B018
        found = (
            self.env["res.partner"]
            .with_user(self.merchant)
            .search([("id", "=", self.admin.partner_id.id)])
        )
        self.assertFalse(found)

    def test_own_contact_is_visible_even_if_admin(self):
        # An administrator is never blocked from seeing themselves.
        self.assertEqual(
            self.admin.partner_id.with_user(self.admin).name,
            self.admin.partner_id.sudo().name,
        )

    def test_admin_sees_other_admin(self):
        other_admin = new_test_user(
            self.env, login="hide_admin_other_admin", groups="base.group_system"
        )
        self.assertEqual(
            other_admin.partner_id.with_user(self.admin).name,
            other_admin.partner_id.sudo().name,
        )

    def test_setting_toggle_disables_restriction(self):
        rule = self.env.ref(
            "partner_hide_admin_contact.res_partner_rule_hide_admin_contact"
        )
        rule.sudo().active = False
        try:
            found = (
                self.env["res.partner"]
                .with_user(self.merchant)
                .search([("id", "=", self.admin.partner_id.id)])
            )
            self.assertTrue(found)
        finally:
            rule.sudo().active = True
