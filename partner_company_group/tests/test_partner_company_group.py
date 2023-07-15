# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestPartnerCompanyGroup(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.company = cls.partner_model.create(
            {"name": "Test Company", "company_type": "company"}
        )
        cls.contact = cls.partner_model.create(
            {"name": "Test Contact", "type": "contact", "parent_id": cls.company.id}
        )
        currency = cls.env.ref("base.USD")
        cls.pricelist1 = cls.env["product.pricelist"].create(
            {"name": "Pricelist 01", "currency_id": currency.id}
        )
        cls.pricelist2 = cls.env["product.pricelist"].create(
            {"name": "Pricelist 02", "currency_id": currency.id}
        )
        cls.company_group1 = cls.env["res.partner"].create(
            {
                "name": "Company Group 01",
                "is_company": True,
                "property_product_pricelist": cls.pricelist1.id,
            }
        )
        cls.company_group2 = cls.env["res.partner"].create(
            {
                "name": "Company Group 02",
                "is_company": True,
                "property_product_pricelist": cls.pricelist2.id,
            }
        )
        cls.partner1 = cls.env["res.partner"].create(
            {
                "name": "Partner 01",
                "is_company": True,
                "property_product_pricelist": cls.pricelist1.id,
                "company_group_id": cls.company_group1.id,
            }
        )
        cls.partner2 = cls.env["res.partner"].create(
            {
                "name": "Partner 02",
                "is_company": True,
                "property_product_pricelist": cls.pricelist1.id,
                "company_group_id": cls.company_group1.id,
            }
        )

    def test_partner_company_group(self):
        self.company.write({"company_group_id": self.company.id})
        self.assertEqual(self.company.company_group_id, self.contact.company_group_id)

    def test_01_change_pricelist_partner(self):
        self.partner1.property_product_pricelist = self.pricelist2
        res = self.partner1._onchange_property_product_pricelist()
        self.assertEqual(
            {
                "warning": {
                    "title": "Warning",
                    "message": "The company group Company Group 01 has the pricelist "
                    "Pricelist 01 (USD), that is different than the "
                    "pricelist set on this contact",
                }
            },
            res,
        )
        self.partner1.property_product_pricelist = self.pricelist1
        res = self.partner1._onchange_property_product_pricelist()
        self.assertEqual({}, res)

    def test_02_change_company_group_partner(self):
        self.partner1.company_group_id = self.company_group2
        res = self.partner1._onchange_company_group_id()
        self.assertEqual(
            {
                "warning": {
                    "title": "Warning",
                    "message": "The company group Company Group 02 has the pricelist "
                    "Pricelist 02 (USD), that is different than the "
                    "pricelist set on this contact",
                }
            },
            res,
        )
        self.partner1.company_group_id = self.company_group1
        res = self.partner1._onchange_company_group_id()
        self.assertEqual({}, res)

    def test_03_change_pricelist_company_group(self):
        self.company_group1.property_product_pricelist = self.pricelist2
        res = self.company_group1._onchange_property_product_pricelist()
        self.assertEqual(
            {
                "warning": {
                    "title": "Warning",
                    "message": "This contact has members of a company group with "
                    "different pricelists, the members are:\n"
                    "\t- Partner 01\n\t- Partner 02\n",
                }
            },
            res,
        )
        self.partner1.property_product_pricelist = self.pricelist2
        res = self.company_group1._onchange_property_product_pricelist()
        self.assertEqual(
            {
                "warning": {
                    "title": "Warning",
                    "message": "This contact has members of a company group with "
                    "different pricelists, the members are:\n"
                    "\t- Partner 02\n",
                }
            },
            res,
        )
        self.partner2.property_product_pricelist = self.pricelist2
        res = self.company_group1._onchange_property_product_pricelist()
        self.assertEqual({}, res)
