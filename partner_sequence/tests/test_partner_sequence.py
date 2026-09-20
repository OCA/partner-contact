from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerSequence(TransactionCase):
    def test_partner_customer_sequence(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "is_customer": True,
            }
        )
        self.assertTrue(partner.x_customer_id, "Customer ID should be generated")

    def test_partner_vendor_sequence(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Vendor",
                "is_vendor": True,
            }
        )
        self.assertTrue(partner.x_vendor_id, "Vendor ID should be generated")

    def test_unique_vat(self):
        self.env["res.partner"].create(
            {
                "name": "Partner A",
                "vat": "123456789",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Partner B",
                    "vat": "123456789",
                }
            )
