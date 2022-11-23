# Copyright 2022 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestPartnertSupplierInfo(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Test partner 1",
                "email": "partner1@test.com",
            }
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Test partner 2",
                "email": "partner2@test.com",
                "is_company": True,
                "ref": "1111",
            }
        )
        cls.partner_3 = cls.env["res.partner"].create(
            {
                "name": "Test partner 3",
                "ref": "0000",
                "email": "partner3@test.com",
                "is_company": True,
            }
        )
        cls.env["partner.supplierinfo"].create(
            {
                "ref": "1234",
                "partner_id": cls.partner_1.id,
                "supplier_id": cls.partner_2.id,
            }
        )
        cls.env["partner.supplierinfo"].create(
            {
                "ref": "4567",
                "partner_id": cls.partner_1.id,
                "supplier_id": cls.partner_3.id,
            }
        )
        cls.env["partner.supplierinfo"].create(
            {
                "ref": "8910",
                "partner_id": cls.partner_3.id,
                "supplier_id": cls.partner_1.id,
            }
        )

    def test_compute_ref(self):
        supplier_ref = self.partner_1.with_context(
            supplier_id=self.partner_2.id
        ).supplier_ref
        self.assertEqual(
            supplier_ref, "1234", "Supplier ref should be the supplier reference"
        )
        supplier_ref = self.partner_1.with_context(
            supplier_id=self.partner_3.id
        ).supplier_ref
        self.assertEqual(
            supplier_ref, "4567", "Supplier ref should be the supplier reference"
        )
        supplier_ref = self.partner_3.with_context(
            supplier_id=self.partner_1.id
        ).supplier_ref
        self.assertEqual(
            supplier_ref, "8910", "Supplier ref should be the supplier reference"
        )
        supplier_ref = self.partner_2.supplier_ref
        self.assertEqual(
            supplier_ref, "1111", "Partner ref should be the partner reference"
        )
