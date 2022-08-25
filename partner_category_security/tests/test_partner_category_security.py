# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, new_test_user


class TestPartnerCategorySecurity(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.basic_user = new_test_user(
            cls.env,
            login="Test basic user",
        )
        cls.partner_category_user = new_test_user(
            cls.env,
            login="Test partner category user",
            groups="partner_category_security.group_partner_category_user",
        )
        cls.partner_category_manager = new_test_user(
            cls.env,
            login="Test partner category manager",
            groups="partner_category_security.group_partner_category_manager",
        )
        cls.partner_category_model = cls.env["res.partner.category"]

    def test_check_access_rights_basic_user(self):
        model = self.partner_category_model.with_user(self.basic_user)
        self.assertTrue(model.check_access_rights("read", False))
        self.assertFalse(model.check_access_rights("write", False))
        self.assertFalse(model.check_access_rights("create", False))
        self.assertFalse(model.check_access_rights("unlink", False))

    def test_check_access_rights_partner_category_user(self):
        model = self.partner_category_model.with_user(self.partner_category_user)
        self.assertTrue(model.check_access_rights("read", False))
        self.assertTrue(model.check_access_rights("write", False))
        self.assertFalse(model.check_access_rights("create", False))
        self.assertFalse(model.check_access_rights("unlink", False))

    def test_check_access_rights_partner_category_manager(self):
        model = self.partner_category_model.with_user(self.partner_category_manager)
        self.assertTrue(model.check_access_rights("read", False))
        self.assertTrue(model.check_access_rights("write", False))
        self.assertTrue(model.check_access_rights("create", False))
        self.assertTrue(model.check_access_rights("unlink", False))
