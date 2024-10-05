# Copyright 2023 Álvaro Marcos <alvaro.marcos@factorlibre.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestSupplierRank(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create({"name": "Test Supplier"})
        cls.purchase_env = cls.env["purchase.order"]

    def test_supplier_rank(self):
        """Check supplier_rank after creation of purchase orders"""
        self.assertEqual(self.supplier.supplier_rank, 0)
        self.purchase_env.create(
            {"name": "Test Purchase 1", "partner_id": self.supplier.id}
        )
        self.assertEqual(self.supplier.supplier_rank, 1)
        self.purchase_env.create(
            [
                {"name": "Test Purchase 2", "partner_id": self.supplier.id},
                {"name": "Test Purchase 3", "partner_id": self.supplier.id},
            ]
        )
        self.assertEqual(self.supplier.supplier_rank, 3)
