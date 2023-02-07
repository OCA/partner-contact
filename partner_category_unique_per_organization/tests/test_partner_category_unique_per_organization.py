# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerCategorySecurity(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_category_main_contact = cls.env["res.partner.category"].create(
            {
                "name": "Main Contact",
                "unique_per_organization": True,
            }
        )
        cls.partner_category_secondary_contact = cls.env["res.partner.category"].create(
            {
                "name": "Secondary Contact",
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
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Test 2",
                "parent_id": cls.org.id,
            }
        )

    def test_partner_category_main(self):
        self.partner_1.category_id |= self.partner_category_main_contact
        with self.assertRaises(UserError):
            self.partner_2.category_id |= self.partner_category_main_contact

    def test_partner_category_secondary(self):
        self.partner_1.category_id |= self.partner_category_secondary_contact
        self.partner_2.category_id |= self.partner_category_secondary_contact
