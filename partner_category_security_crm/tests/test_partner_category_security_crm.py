# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import new_test_user

from odoo.addons.partner_category_security.tests.test_partner_category_security import (
    TestPartnerCategorySecurity,
)


class TestPartnerCategorySecurityCrm(TestPartnerCategorySecurity):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesman_user = new_test_user(
            cls.env,
            login="Test salesmane",
            groups="sales_team.group_sale_salesman",
        )

    def test_check_access_rights_salesman_user(self):
        model = self.partner_category_model.with_user(self.salesman_user)
        self.assertTrue(model.check_access_rights("read", False))
        self.assertFalse(model.check_access_rights("write", False))
        self.assertFalse(model.check_access_rights("create", False))
        self.assertFalse(model.check_access_rights("unlink", False))
