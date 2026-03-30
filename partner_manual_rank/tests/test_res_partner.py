from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("res_partner")
class TestResPartner(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partner = self.env["res.partner"]
        self.partner = self.Partner.create({"name": "Microsoft Corporation"})
        self.partner_2 = self.Partner.create({"name": "Apple Inc."})
        self.car = self.env["product.product"].create(
            {
                "name": "Car",
            }
        )

    def _create_invoice(self, move_type, date, partner_id, **kwargs):
        move = self.env["account.move"].create(
            {
                "invoice_date": date,
                "partner_id": partner_id.id,
                **kwargs,
                "move_type": move_type,
                "date": date,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.car.id,
                            "price_unit": 120.0,
                            "tax_ids": [],
                            **line_kwargs,
                        }
                    )
                    for line_kwargs in kwargs.get("invoice_line_ids", [{}])
                ],
            }
        )
        return move.action_post()

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
        partners.write({"customer_rank": 1})
        self.assertRecordValues(
            partners,
            [
                {"is_customer": True, "customer_rank": 1},
                {"is_customer": True, "customer_rank": 1},
            ],
        )
        with self.assertRaisesRegex(UserError, "Operation not supported"):
            self.env["res.partner"].search([("is_customer", "in", [True, False])])

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
        with self.assertRaisesRegex(UserError, "Operation not supported"):
            self.env["res.partner"].search([("is_supplier", "in", [True, False])])

    def test_setting_customer_ranking(self):
        # By default (standard) invoice creation should increase the ``customer_rank``
        self._create_invoice(
            move_type="out_invoice", date=fields.Date.today(), partner_id=self.partner
        )
        self.assertEqual(self.partner.customer_rank, 1)
        # Disable automatic ranking should prevent increasing the rank
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_manual_rank.partner_rank_auto", False
        )
        self._create_invoice(
            move_type="out_invoice", date=fields.Date.today(), partner_id=self.partner
        )
        self.assertEqual(self.partner.customer_rank, 1)
        # Enable again automatic ranking
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_manual_rank.partner_rank_auto", True
        )
        self._create_invoice(
            move_type="out_invoice", date=fields.Date.today(), partner_id=self.partner
        )
        self.assertEqual(self.partner.customer_rank, 2)

    def test_setting_supplier_ranking(self):
        # By default (standard) invoice creation should increase the ``supplier_rank``
        self._create_invoice(
            move_type="in_invoice", date=fields.Date.today(), partner_id=self.partner_2
        )
        self.assertEqual(self.partner_2.supplier_rank, 1)
        # Disable automatic ranking should prevent increasing the rank
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_manual_rank.partner_rank_auto", False
        )
        self._create_invoice(
            move_type="in_invoice", date=fields.Date.today(), partner_id=self.partner_2
        )
        self.assertEqual(self.partner_2.supplier_rank, 1)
        # Enable again automatic ranking
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_manual_rank.partner_rank_auto", True
        )
        self._create_invoice(
            move_type="in_invoice", date=fields.Date.today(), partner_id=self.partner_2
        )
        self.assertEqual(self.partner_2.supplier_rank, 2)
