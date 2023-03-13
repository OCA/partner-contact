# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPartnerCategoryInherit(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_category_simple = cls.env["res.partner.category"].create(
            {
                "name": "Partner Category simple",
            }
        )
        cls.partner_category_inherited = cls.env["res.partner.category"].create(
            {
                "name": "Partner Category inherited",
                "inherited": True,
            }
        )
        cls.org = cls.env["res.partner"].create(
            {
                "name": "Org",
                "is_company": True,
            }
        )
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Test 1",
                "parent_id": cls.org.id,
            }
        )

    def test_partner_category_inherited(self):
        self.org.category_id |= self.partner_category_inherited
        self.assertTrue(self.partner_category_inherited in self.org.category_id)
        self.assertTrue(self.partner_category_inherited in self.partner_1.category_id)
        self.org.category_id -= self.partner_category_inherited
        self.assertFalse(self.partner_category_inherited in self.org.category_id)
        self.assertFalse(self.partner_category_inherited in self.partner_1.category_id)

    def test_partner_category_inherited_on_creation(self):
        self.org.category_id |= self.partner_category_inherited
        self.partner_2 = self.env["res.partner"].create(
            {
                "name": "Test 2",
                "parent_id": self.org.id,
            }
        )
        self.assertTrue(self.partner_category_inherited in self.partner_2.category_id)

    def test_partner_category_not_inherited(self):
        self.org.category_id |= self.partner_category_simple
        self.assertTrue(self.partner_category_simple in self.org.category_id)
        self.assertFalse(self.partner_category_simple in self.partner_1.category_id)
