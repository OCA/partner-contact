from odoo.tests import common


class TestWizard(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a mock res.partner record
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Mock Partner",
                "phone": "937654321",
            }
        )
        cls.partner_obj = cls.env["res.partner"]

    def test_button_opens_wizard(self):
        partners = self.partner_obj.search([("phone", "=", "937654321")])

        # Simulate button click
        wizard_information = self.partner.generate_qr_code_wizard()
        # # Assert wizard opening
        self.assertEqual(
            wizard_information["name"], "%s's Contact QR Code" % partners.name
        )
        self.assertEqual(wizard_information["res_model"], "contacts.qr.code")
        self.assertEqual(wizard_information["view_type"], "form")
        self.assertEqual(partners, self.partner)
