# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from lxml import etree

from odoo.tests import new_test_user
from odoo.tests.common import users

from odoo.addons.base.tests.common import BaseCommon


class TestPartnerCategorySecurity(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.basic_user = new_test_user(
            cls.env,
            login="test_basic_user",
        )
        cls.partner_category_user = new_test_user(
            cls.env,
            login="test_partner_category_user",
            groups="partner_category_security.group_partner_category_user",
        )
        cls.partner_category_manager = new_test_user(
            cls.env,
            login="test_partner_category_manager",
            groups="partner_category_security.group_partner_category_manager",
        )
        cls.partner_model = cls.env["res.partner"]
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
        self.assertFalse(model.check_access_rights("write", False))
        self.assertFalse(model.check_access_rights("create", False))
        self.assertFalse(model.check_access_rights("unlink", False))

    def test_check_access_rights_partner_category_manager(self):
        model = self.partner_category_model.with_user(self.partner_category_manager)
        self.assertTrue(model.check_access_rights("read", False))
        self.assertTrue(model.check_access_rights("write", False))
        self.assertTrue(model.check_access_rights("create", False))
        self.assertTrue(model.check_access_rights("unlink", False))

    @users("test_basic_user")
    def test_partner_model_fields_view_get_1(self):
        res = self.partner_model.with_user(self.env.user).get_view(view_type="form")
        node = etree.XML(res["arch"]).xpath("//field[@name='category_id']")[0]
        modifiers = json.loads(node.get("modifiers"))
        self.assertTrue(modifiers["readonly"])
        self.assertEqual(node.get("force_save"), "1")

    @users("test_partner_category_user")
    def test_partner_model_fields_view_get_2(self):
        res = self.partner_model.with_user(self.env.user).get_view(view_type="form")
        node = etree.XML(res["arch"]).xpath("//field[@name='category_id']")[0]
        modifiers = json.loads(node.get("modifiers")) if node.get("modifiers") else {}
        self.assertTrue("readonly" not in modifiers or not modifiers["readonly"])
        self.assertFalse(node.get("force_save"))

    @users("test_partner_category_manager")
    def test_partner_model_fields_view_get_3(self):
        res = self.partner_model.with_user(self.env.user).get_view(view_type="form")
        node = etree.XML(res["arch"]).xpath("//field[@name='category_id']")[0]
        modifiers = json.loads(node.get("modifiers")) if node.get("modifiers") else {}
        self.assertTrue("readonly" not in modifiers or not modifiers["readonly"])
        self.assertFalse(node.get("force_save"))
