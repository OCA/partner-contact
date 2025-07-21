# Copyright 2025 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.supplier = cls.partner_model.create(
            {
                "name": "Supplier",
                "supplier_ref": "1038",
                "is_company": True,
            }
        )

    def test_supplier_ref_propagation_to_contact(self):
        contact = self.partner_model.create(
            {
                "name": "Contact Person",
                "parent_id": self.supplier.id,
            }
        )
        self.assertEqual(contact.supplier_ref, "1038")

    def test_supplier_ref_not_copied(self):
        partner_copy = self.supplier.copy()
        self.assertFalse(partner_copy.supplier_ref)
