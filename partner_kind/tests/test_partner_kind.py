# Copyright 2023 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerKind(TransactionCase):
    def setUp(self):
        super(TestPartnerKind, self).setUp()

        self.Partner1 = self.env.ref("base.res_partner_address_15")
        self.Partner2 = self.env.ref("base.partner_admin")
        self.Partner3 = self.env.ref("base.res_partner_12")

    def test_partner_user_kind(self):

        self.assertEqual(self.Partner2.kind, "user")

    def test_partner_address_kind(self):

        self.assertEqual(self.Partner1.kind, "address")

    def test_partner_company_kinds(self):

        self.assertEqual(self.Partner3.kind, "company")

    def test_partner_person_kind(self):

        self.Partner1.write(
            {
                "parent_id": False,
            }
        )
        self.assertEqual(self.Partner1.kind, "person")

    def test_default_kind(self):

        self.Partner4 = self.env["res.partner"].create(
            {
                "name": "TestPartner4",
            }
        )
        self.assertEqual(self.Partner4.kind, "company")

    def test_partner_user_error(self):

        with self.assertRaises(ValidationError) as error:
            self.Partner3.write(
                {
                    "kind": "user",
                }
            )
        message = error.exception.args[0]
        self.assertEqual(message, "User type is only for users")

    def test_partner_address_error(self):

        with self.assertRaises(ValidationError) as error:
            self.Partner3.write(
                {
                    "kind": "address",
                }
            )
        message = error.exception.args[0]
        self.assertEqual(message, "Company field is mandatory for address type")
