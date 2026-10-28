# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBasePartnerSequenceManualRank(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]

    def test_ref_not_assigned_when_not_customer(self):
        partner = self.partner_model.create(
            {
                "name": "Supplier A",
                "is_company": True,
                "is_supplier": True,
            }
        )
        self.assertFalse(partner.ref)

    def test_ref_assigned_when_customer(self):
        partner = self.partner_model.create(
            {
                "name": "Customer A",
                "is_company": True,
                "is_customer": True,
            }
        )
        self.assertTrue(partner.ref)

    def test_ref_assigned_when_customer_and_supplier(self):
        partner = self.partner_model.create(
            {
                "name": "Customer Supplier A",
                "is_company": True,
                "is_customer": True,
                "is_supplier": True,
            }
        )
        self.assertTrue(partner.ref)

    def test_ref_not_assigned_on_copy_when_not_customer(self):
        original = self.partner_model.create(
            {
                "name": "Supplier B",
                "is_company": True,
                "is_supplier": True,
            }
        )
        copy = original.copy()
        self.assertFalse(copy.ref)

    def test_ref_assigned_on_copy_when_customer(self):
        original = self.partner_model.create(
            {
                "name": "Customer A",
                "is_company": True,
                "is_customer": True,
            }
        )
        # The is_customer is not copied, so the ref
        # should not be set with the sequence
        copy = original.copy()
        self.assertFalse(copy.ref)

    def test_ref_assigned_on_write_when_becomes_customer(self):
        partner = self.partner_model.create(
            {
                "name": "Partner A",
                "is_company": True,
            }
        )
        self.assertFalse(partner.ref)
        partner.write({"is_customer": True})
        self.assertTrue(partner.ref)
