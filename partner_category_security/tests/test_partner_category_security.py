# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests import new_test_user
from odoo.tests.common import Form

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
        cls.partner_category_model = cls.env["res.partner.category"]
        cls.test_category = cls.partner_category_model.create({"name": "Test category"})

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

    def test_partner_model_fields_view_get_1(self):
        """Basic users can only read categories, but not set them."""
        self.basic_user.groups_id |= self.browse_ref("base.group_partner_manager")
        with Form(self.partner.with_user(self.basic_user)) as partner_f:
            self.assertFalse(partner_f.category_id)
            with self.assertRaises(AssertionError):
                partner_f.category_id.add(self.test_category)

    def test_partner_model_fields_view_get_2(self):
        """Category users can set categories."""
        self.partner_category_user.groups_id |= self.browse_ref(
            "base.group_partner_manager"
        )
        with Form(self.partner.with_user(self.partner_category_user)) as partner_f:
            self.assertFalse(partner_f.category_id)
            partner_f.category_id.add(self.test_category)
        self.assertEqual(self.partner.category_id, self.test_category)

    def test_partner_model_fields_view_get_3(self):
        """Managers can set categories."""
        self.partner_category_manager.groups_id |= self.browse_ref(
            "base.group_partner_manager"
        )
        with Form(self.partner.with_user(self.partner_category_manager)) as partner_f:
            self.assertFalse(partner_f.category_id)
            partner_f.category_id.add(self.test_category)
        self.assertEqual(self.partner.category_id, self.test_category)

    def test_ir_ui_menu(self):
        menu_partner_category_custom = self.env.ref(
            "partner_category_security.menu_partner_category_custom"
        )
        visible_ids = (
            self.env["ir.ui.menu"].with_user(self.basic_user)._visible_menu_ids()
        )
        self.assertNotIn(menu_partner_category_custom.id, visible_ids)
        visible_ids = (
            self.env["ir.ui.menu"]
            .with_user(self.partner_category_user)
            ._visible_menu_ids()
        )
        self.assertNotIn(menu_partner_category_custom.id, visible_ids)
        visible_ids = (
            self.env["ir.ui.menu"]
            .with_user(self.partner_category_manager)
            ._visible_menu_ids()
        )
        self.assertIn(menu_partner_category_custom.id, visible_ids)
        # Add system to partner_category_manager user
        self.partner_category_manager.write(
            {"groups_id": [(4, self.env.ref("base.group_system").id)]}
        )
        visible_ids = (
            self.env["ir.ui.menu"]
            .with_user(self.partner_category_manager)
            ._visible_menu_ids()
        )
        self.assertNotIn(menu_partner_category_custom.id, visible_ids)
