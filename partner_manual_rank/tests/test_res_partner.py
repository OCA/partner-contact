from odoo.tests import common, tagged


@tagged("res_partner")
class TestResPartner(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Microsoft Corporation"})
        self.partner_2 = self.env["res.partner"].create({"name": "Apple Inc."})

    def test_create_with_rank(self):
        p = self.env["res.partner"].create({"name": "customer", "customer_rank": 1})
        self.assertTrue(p.is_customer)
        self.assertEqual(p.customer_rank, 1)
        self.assertFalse(p.is_supplier)
        self.assertEqual(p.supplier_rank, 0)
        p = self.env["res.partner"].create({"name": "supplier", "supplier_rank": 1})
        self.assertTrue(p.is_supplier)
        self.assertEqual(p.supplier_rank, 1)
        self.assertFalse(p.is_customer)
        self.assertEqual(p.customer_rank, 0)

    def test_create_without_rank(self):
        p = self.env["res.partner"].create({"name": "customer", "is_customer": True})
        self.assertTrue(p.is_customer)
        self.assertEqual(p.customer_rank, 1)
        self.assertFalse(p.is_supplier)
        self.assertEqual(p.supplier_rank, 0)
        p = self.env["res.partner"].create({"name": "supplier", "is_supplier": True})
        self.assertTrue(p.is_supplier)
        self.assertEqual(p.supplier_rank, 1)
        self.assertFalse(p.is_customer)
        self.assertEqual(p.customer_rank, 0)

    def test_01_is_customer(self):
        partners = self.partner | self.partner_2
        self.assertRecordValues(
            partners,
            [
                {"is_customer": False, "customer_rank": 0},
                {"is_customer": False, "customer_rank": 0},
            ],
        )
        self.partner.write({"is_customer": True})
        self.assertRecordValues(
            partners,
            [
                {"is_customer": True, "customer_rank": 1},
                {"is_customer": False, "customer_rank": 0},
            ],
        )
        partners_found = self.env["res.partner"].search([("is_customer", "=", True)])
        self.assertIn(self.partner, partners_found)
        partners.write({"is_customer": True})
        self.assertRecordValues(
            partners,
            [
                {"is_customer": True, "customer_rank": 1},
                {"is_customer": True, "customer_rank": 1},
            ],
        )
        partners.write({"is_customer": False})
        self.assertRecordValues(
            partners,
            [
                {"is_customer": False, "customer_rank": 0},
                {"is_customer": False, "customer_rank": 0},
            ],
        )

    def test_02_is_supplier(self):
        partners = self.partner | self.partner_2
        self.assertRecordValues(
            partners,
            [
                {"is_supplier": False, "supplier_rank": 0},
                {"is_supplier": False, "supplier_rank": 0},
            ],
        )
        self.partner.write({"is_supplier": True})
        self.assertRecordValues(
            partners,
            [
                {"is_supplier": True, "supplier_rank": 1},
                {"is_supplier": False, "supplier_rank": 0},
            ],
        )
        partners_found = self.env["res.partner"].search([("is_supplier", "=", True)])
        self.assertIn(self.partner, partners_found)
        partners.write({"is_supplier": True})
        self.assertRecordValues(
            partners,
            [
                {"is_supplier": True, "supplier_rank": 1},
                {"is_supplier": True, "supplier_rank": 1},
            ],
        )
        partners.write({"is_supplier": False})
        self.assertRecordValues(
            partners,
            [
                {"is_supplier": False, "supplier_rank": 0},
                {"is_supplier": False, "supplier_rank": 0},
            ],
        )
