# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestResPartnerSupplierRefSequence(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_supplier_ref_on_create(self):
        partner = self.partner_model.create(
            {
                "name": "Supplier A",
                "is_company": True,
            }
        )
        self.assertFalse(partner.supplier_ref)

        partner = self.partner_model.create(
            {
                "name": "Supplier B",
                "is_company": True,
                "is_supplier": True,
            }
        )
        self.assertTrue(partner.supplier_ref)

    def test_supplier_ref_on_copy(self):
        original = self.partner_model.create(
            {
                "name": "Original Supplier",
                "is_supplier": True,
                "is_company": True,
            }
        )
        copy = original.copy()
        self.assertNotEqual(original.supplier_ref, copy.supplier_ref)
        self.assertTrue(copy.supplier_ref)

    def test_supplier_ref_on_write(self):
        partner = self.partner_model.create(
            {
                "name": "Some Partner",
            }
        )
        self.assertFalse(partner.supplier_ref)
        partner.write(
            {
                "is_supplier": True,
                "is_company": True,
            }
        )
        self.assertTrue(partner.supplier_ref)

    def test_supplier_ref_not_overwritten_if_set(self):
        partner = self.partner_model.create(
            {
                "name": "Preset Ref",
                "is_company": True,
                "supplier_ref": "1234",
            }
        )
        self.assertEqual(partner.supplier_ref, "1234")
        partner.write(
            {
                "is_supplier": True,
            }
        )
        self.assertEqual(partner.supplier_ref, "1234")
