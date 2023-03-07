# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import common


class TestPartnerCategoryRestrict(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.filter_company_only = cls.env["ir.filters"].create(
            {
                "name": "company only",
                "model_id": "res.partner",
                "domain": "[['is_company','=',True]]",
            }
        )
        cls.partner_category_simple = cls.env["res.partner.category"].create(
            {
                "name": "Partner Category simple",
            }
        )
        cls.partner_category_company_only = cls.env["res.partner.category"].create(
            {
                "name": "Partner Category company only",
                "restrict_filter_id": cls.filter_company_only.id,
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

    def test_partner_category_restricted(self):
        self.org.category_id |= self.partner_category_company_only
        with self.assertRaises(UserError):
            self.partner_1.category_id |= self.partner_category_company_only

    def test_partner_category_not_restricted(self):
        self.org.category_id |= self.partner_category_simple
        self.partner_1.category_id |= self.partner_category_simple
