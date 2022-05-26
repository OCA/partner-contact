from odoo.tests import common, tagged


@tagged("res_partner")
class TestResPartner(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Microsoft Corporation"})
        self.partner_2 = self.env["res.partner"].create({"name": "Apple Inc."})

    def test_customer(self):
        partners = self.partner | self.partner_2
        self.assertRecordValues(
            partners,
            [
                {"customer": False, "customer_rank": 0},
                {"customer": False, "customer_rank": 0},
            ],
        )
        self.partner.write({"customer": True})
        self.assertRecordValues(
            partners,
            [
                {"customer": True, "customer_rank": 1},
                {"customer": False, "customer_rank": 0},
            ],
        )
        partners_found = self.env["res.partner"].search([("customer", "=", True)])
        self.assertIn(self.partner, partners_found)
        partners.write({"customer": True})
        self.assertRecordValues(
            partners,
            [
                {"customer": True, "customer_rank": 1},
                {"customer": True, "customer_rank": 1},
            ],
        )
        partners.write({"customer": False})
        self.assertRecordValues(
            partners,
            [
                {"customer": False, "customer_rank": 0},
                {"customer": False, "customer_rank": 0},
            ],
        )

    def test_supplier(self):
        partners = self.partner | self.partner_2
        self.assertRecordValues(
            partners,
            [
                {"supplier": False, "supplier_rank": 0},
                {"supplier": False, "supplier_rank": 0},
            ],
        )
        self.partner.write({"supplier": True})
        self.assertRecordValues(
            partners,
            [
                {"supplier": True, "supplier_rank": 1},
                {"supplier": False, "supplier_rank": 0},
            ],
        )
        partners_found = self.env["res.partner"].search([("supplier", "=", True)])
        self.assertIn(self.partner, partners_found)
        partners.write({"supplier": True})
        self.assertRecordValues(
            partners,
            [
                {"supplier": True, "supplier_rank": 1},
                {"supplier": True, "supplier_rank": 1},
            ],
        )
        partners.write({"supplier": False})
        self.assertRecordValues(
            partners,
            [
                {"supplier": False, "supplier_rank": 0},
                {"supplier": False, "supplier_rank": 0},
            ],
        )
