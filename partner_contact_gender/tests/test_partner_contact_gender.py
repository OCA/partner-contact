# Copyright 2016-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPartnerContactGender(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_partner = cls.env["res.partner"].create(
            {"name": "Test Partner 1", "gender": "female"}
        )

    def test_partner_contact_gender(self):
        self.assertEqual(self.test_partner.gender, "female")
