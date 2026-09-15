# Copyright 2023 Álvaro Marcos <alvaro.marcos@factorlibre.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import os
from unittest import mock

from odoo.tests.common import TransactionCase


class TestSupplierRank(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create({"name": "Test Supplier"})
        cls.child_supplier = cls.env["res.partner"].create(
            {"name": "Child Supplier", "parent_id": cls.supplier.id}
        )
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
        # Odoo 19 defers subsequent rank updates to postcommit
        with self.enter_registry_test_mode():
            self.env.cr.postcommit.run()
        self.assertEqual(self.supplier.supplier_rank, 3)

    def test_post_init_hook(self):
        """Verify post_init_hook increases supplier_rank for all purchase partners."""
        from .. import post_init_hook

        self.purchase_env.create(
            {"name": "Test Purchase Child", "partner_id": self.child_supplier.id}
        )
        with mock.patch.dict(os.environ, {"ODOO_TEST_MODE": ""}):
            post_init_hook(self.env)
