# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestPartnerAddressOk(TransactionCase):
    def setUp(self):
        super().setUp()
        self.testpartner_ok = self.env["res.partner"].create(
            {"name": "test", "address_ok": True}
        )
        self.testpartner_not_ok = self.env["res.partner"].create(
            {"name": "test", "address_ok": False}
        )

    def test_partner_address(self):
        self.assertEqual(self.testpartner_ok.address_ok, True)
        self.assertEqual(self.testpartner_not_ok.address_ok, False)
