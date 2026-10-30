from odoo.tests import common, tagged


@tagged("res_partner")
class TestResPartner(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partner = self.env["res.partner"]
        self.partner = self.Partner.create({"name": "Microsoft Corporation"})
        self.partner_2 = self.Partner.create({"name": "Apple Inc."})

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
        partners_found = self.Partner.search([("is_customer", "=", True)])
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
        partners.write({"customer_rank": 1})
        self.assertRecordValues(
            partners,
            [
                {"is_customer": True, "customer_rank": 1},
                {"is_customer": True, "customer_rank": 1},
            ],
        )
        # unsupported operator
        res = self.Partner._search_is_customer("like", True)
        self.assertIs(res, NotImplemented)

        # unsupported value type
        res = self.Partner._search_is_customer("=", "True")
        self.assertIs(res, NotImplemented)

        # supported
        res = self.Partner._search_is_customer("=", True)
        self.assertIsInstance(res, list)
        self.assertTrue(res and isinstance(res[0], tuple))

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
        partners.write({"supplier_rank": 1})
        self.assertRecordValues(
            partners,
            [
                {"is_supplier": True, "supplier_rank": 1},
                {"is_supplier": True, "supplier_rank": 1},
            ],
        )
        # unsupported operator
        res = self.Partner._search_is_supplier("like", True)
        self.assertIs(res, NotImplemented)
        # unsupported value type
        res = self.Partner._search_is_supplier("=", "True")
        self.assertIs(res, NotImplemented)
        # supported
        res = self.Partner._search_is_supplier("=", True)
        self.assertIsInstance(res, list)
        self.assertTrue(res and isinstance(res[0], tuple))
