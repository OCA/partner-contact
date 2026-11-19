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
        # PO 1: rank is 0 → incremented immediately to 1
        self.purchase_env.create({"name": "PO 1", "partner_id": self.supplier.id})
        self.assertEqual(self.supplier.supplier_rank, 1)
        # PO 2 & PO 3: rank > 0 → Odoo 19 defers increments to postcommit hook
        self.purchase_env.create(
            [
                {"name": "PO 2", "partner_id": self.supplier.id},
                {"name": "PO 3", "partner_id": self.supplier.id},
            ]
        )
        self.supplier.invalidate_recordset()
        # In tests, postcommit never runs (tx rolled back), so rank stays at 1
        self.assertEqual(self.supplier.supplier_rank, 1)
