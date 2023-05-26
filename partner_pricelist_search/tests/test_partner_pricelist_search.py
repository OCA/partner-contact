# Copyright 2021 Tecnativa - Carlos Dauden
# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import common


class TestPartnerPricelistSearch(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist_1 = cls.env["product.pricelist"].create(
            {"name": "Test pricelist 1"}
        )
        cls.pricelist_2 = cls.env["product.pricelist"].create(
            {"name": "Test pricelist 2"}
        )
        cls.customer_1 = cls.env["res.partner"].create(
            {"name": "Test customer 1", "property_product_pricelist": cls.pricelist_1}
        )
        cls.customer_2 = cls.env["res.partner"].create(
            {"name": "Test customer 2", "property_product_pricelist": cls.pricelist_2}
        )
        cls.partner_obj = cls.env["res.partner"]

    def test_partner_pricelist_search_equal(self):
        """Test search '='"""
        partners = self.partner_obj.search(
            [("property_product_pricelist", "=", self.pricelist_1.id)]
        )
        self.assertEqual(partners, self.customer_1)

    def test_partner_pricelist_search_in(self):
        """Test search 'in'"""
        partners = self.partner_obj.search(
            [
                (
                    "property_product_pricelist",
                    "in",
                    (self.pricelist_1 | self.pricelist_2).ids,
                )
            ]
        )
        self.assertIn(self.customer_1, partners)
        self.assertIn(self.customer_2, partners)

    def test_partner_pricelist_search_not_equal(self):
        """Test search 'not equal'"""
        partners = self.partner_obj.search(
            [("property_product_pricelist", "!=", self.pricelist_1.id)]
        )
        self.assertNotIn(self.customer_1, partners)
        self.assertIn(self.customer_2, partners)

    def test_partner_pricelist_search_not_in(self):
        """Test search 'not in'"""
        partners = self.partner_obj.search(
            [
                (
                    "property_product_pricelist",
                    "not in",
                    (self.pricelist_1 | self.pricelist_2).ids,
                )
            ]
        )
        self.assertNotIn(self.customer_1, partners)
        self.assertNotIn(self.customer_2, partners)

    def test_partner_pricelist_search_ilike(self):
        """Test search 'ilike'"""
        partners = self.partner_obj.search(
            [("property_product_pricelist", "ilike", "Test pricelist 1")]
        )
        self.assertIn(self.customer_1, partners)
        self.assertNotIn(self.customer_2, partners)

    def test_show_pricelist_partners(self):
        res = self.pricelist_1.show_pricelist_partners()
        self.assertEqual(self.partner_obj.search(res["domain"]), self.customer_1)
        res = (self.pricelist_1 | self.pricelist_2).show_pricelist_partners()
        self.assertEqual(
            self.partner_obj.search(res["domain"]), (self.customer_1 | self.customer_2)
        )
