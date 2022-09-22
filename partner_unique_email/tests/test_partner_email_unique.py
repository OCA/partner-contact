from odoo.exceptions import ValidationError
from odoo.tests import common
from odoo.tools import config


class TestResPartnerEmailUniqueCommon(common.TransactionCase):
    def setUp(self):
        super(TestResPartnerEmailUniqueCommon, self).setUp()

        partner_obj = self.env["res.partner"].with_context(
            {"test_partner_email_unique": True}
        )

        self.partner1 = partner_obj.create({"name": "Partner1"})
        self.partner2 = partner_obj.create({"name": "Partner2"})

    def test_check_unique_email(self):

        self.partner1.email = "same_email@test.com"
        self.partner2.email = "different_email@test.com"

        self.assertNotEqual(self.partner1.email, self.partner2.email)
        self.partner2.ref = False

        with self.assertRaises(ValidationError):
            self.partner2.email = "same_email@test.com"
        self.env["res.company"].create({"name": "TestCompany"})
        self.partner1.email = False
        self.partner2.email = False
        config["test_enable"] = True

    def test_copy_does_not_raise_duplicate_email_error(self):
        self.partner1.copy()
