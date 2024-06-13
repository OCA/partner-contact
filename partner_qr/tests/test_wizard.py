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

        # Set the context with 'active_model' and 'active_id'
        context = {"active_model": "res.partner", "active_id": 26}
        # Create a mock contacts.qr.code record
        cls.wizard = (
            cls.env["contacts.qr.code"]
            .with_context(**context)
            .create(
                {
                    "fullname": "True",
                    "company_name": "True",
                    "job_title": "True",
                    "email": "True",
                    "url": "True",
                }
            )
        )
        cls.wizard_obj = cls.env["contacts.qr.code"]

    def test_button_opens_wizard(self):
        partners = self.partner_obj.search([("phone", "=", "937654321")])

        # Simulate button click
        wizard_information = self.partner.generate_qr_code_wizard()

        # Assert wizard opening
        self.assertEqual(
            wizard_information["name"],
            "%s's Contact QR Code" % partners.name,
        )
        self.assertEqual(wizard_information["res_model"], "contacts.qr.code")
        self.assertEqual(wizard_information["view_type"], "form")
        self.assertEqual(partners, self.partner)

    def test_checkboxes(self):
        # Initially, the checkboxes should be checked
        self.assertTrue(self.wizard.fullname, "Fullname should be checked by default")
        self.assertTrue(
            self.wizard.company_name, "Company Name should be checked by default"
        )
        self.assertTrue(self.wizard.job_title, "Job Title should be checked by default")
        self.assertTrue(self.wizard.email, "email should be checked by default")
        self.assertTrue(self.wizard.url, "URL should be checked by default")

        # Uncheck every checkbox
        self.wizard.write({"fullname": False})
        self.wizard.write({"company_name": False})
        self.wizard.write({"job_title": False})
        self.wizard.write({"email": False})
        self.wizard.write({"url": False})
        self.assertFalse(self.wizard.fullname, "Fullname should be unchecked now")
        self.assertFalse(
            self.wizard.company_name, "Company Name should be unchecked now"
        )
        self.assertFalse(self.wizard.job_title, "Job Title should be unchecked now")
        self.assertFalse(self.wizard.email, "email should be unchecked now")
        self.assertFalse(self.wizard.url, "URL should be unchecked now")

    def test_creates_qr_code(self):
        # Generate the QR Code
        self.wizard._compute_qr_code()
        test_wizard = self.wizard_obj.search([("fullname", "=", "True")])

        # Check if QR Code was created
        self.assertIsInstance(
            test_wizard.qr_code, bytes, "qr_code should be of type 'bytes'"
        )

    def test_download_qr(self):
        # Simulate button click
        wizard_information = self.wizard.download_qr()

        # Assert wizard opening
        self.assertEqual(wizard_information["type"], "ir.actions.act_url")
        self.assertEqual(wizard_information["target"], "form")
