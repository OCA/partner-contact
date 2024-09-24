# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class PartnerCompanyInvoiceAddressCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_obj = cls.env["res.partner"]
        cls.system_parameters = cls.env["ir.config_parameter"]

        cls.partner1 = cls.partner_obj.create({"name": "Partner1", "is_company": True})

        cls.partner2 = cls.partner_obj.create(
            {
                "name": "Partner2",
                "parent_id": cls.partner1.id,
                "type": "other",
            }
        )

    def test_01_partner_invoice_address(self):
        """Test that a partner can have type invoice"""
        self.partner2.parent_id = self.partner1.id
        self.partner2.type = "invoice"
        self.assertEqual(self.partner2.type, "invoice")
        partner3 = self.partner_obj.create({"name": "Test 3", "type": "invoice"})
        self.assertEqual(partner3.type, "invoice")

    def test_02_partner_invoice_address(self):
        """Test that a partner cannot have type invoice"""
        self.system_parameters.set_param("partner_block_invoice_address", True)
        self.system_parameters.set_param(
            "partner_block_invoice_address_default_type", "other"
        )
        with self.assertRaisesRegex(
            Exception,
            "You cannot set a contact as an invoice address. " "Check the settings.",
        ):
            self.partner2.type = "invoice"

            self.partner_obj.create({"name": "Test 3", "type": "invoice"})
