# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.tests import common, tagged

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@tagged("res_partner")
class TestPartnerRankSingle(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context, no_state_required=True, **DISABLED_MAIL_CONTEXT
            )
        )
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Customer",
                "is_company": True,
            }
        )
        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "Supplier",
                "is_company": True,
            }
        )
        cls.table = cls.env["product.product"].create({"name": "Table"})

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
                            "product_id": self.table.id,
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

    def test_00_customer_rank_single(self):
        # No rank yet
        self.assertFalse(self.customer.customer_rank)
        self.assertFalse(self.customer.supplier_rank)
        # Create an invoice as customer
        self._create_invoice(
            move_type="out_invoice", date=fields.Date.today(), partner_id=self.customer
        )
        self.assertEqual(self.customer.customer_rank, 1, "Ranked")
        self.assertFalse(self.customer.supplier_rank, "Not ranked")
        # Create an invoice as supplier
        self._create_invoice(
            move_type="in_invoice",
            date=fields.Date.today(),
            partner_id=self.customer,
        )
        self.assertEqual(self.customer.customer_rank, 1, "Rank unchanged")
        self.assertFalse(self.customer.supplier_rank, "Not ranked")
        # Create another invoice as customer
        self._create_invoice(
            move_type="out_invoice",
            date=fields.Date.today(),
            partner_id=self.customer,
        )
        self.assertEqual(self.customer.customer_rank, 2, "Rank increased")
        self.assertFalse(self.customer.supplier_rank, "Not ranked")

    def test_01_supplier_rank_single(self):
        # No rank yet
        self.assertFalse(self.supplier.customer_rank)
        self.assertFalse(self.supplier.supplier_rank)
        # Create an invoice as supplier
        self._create_invoice(
            move_type="in_invoice",
            date=fields.Date.today(),
            partner_id=self.supplier,
        )
        self.assertEqual(self.supplier.supplier_rank, 1, "Ranked")
        self.assertFalse(self.supplier.customer_rank, "Not ranked")
        # Create an invoice as customer
        self._create_invoice(
            move_type="out_invoice",
            date=fields.Date.today(),
            partner_id=self.supplier,
        )
        self.assertFalse(self.supplier.customer_rank, "Not ranked")
        self.assertEqual(self.supplier.supplier_rank, 1, "Rank unchanged")
        # Create another invoice as supplier
        self._create_invoice(
            move_type="in_invoice",
            date=fields.Date.today(),
            partner_id=self.supplier,
        )
        self.assertEqual(self.supplier.supplier_rank, 2, "Rank increased")
        self.assertFalse(self.supplier.customer_rank, "Not ranked")

    def test_03_customer_rank_manual(self):
        self.customer.customer_rank = 10
        with self.assertRaisesRegex(
            ValidationError, "A contact cannot be both a customer and a supplier."
        ):
            self.customer.supplier_rank = 1

    def test_04_supplier_rank_manual(self):
        self.supplier.supplier_rank = 10
        with self.assertRaisesRegex(
            ValidationError, "A contact cannot be both a customer and a supplier."
        ):
            self.supplier.customer_rank = 1
