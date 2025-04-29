# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test copy function for models."""

from odoo.tests import TransactionCase

from .base import MailInstalled


class UserCase(TransactionCase, MailInstalled):
    """Test ``res.users``."""

    def setUp(self):
        super().setUp()
        self.create_original()
        self.create_original_multinames()

    def create_original(self):
        self.original = self.env["res.users"].create(
            {
                "firstname": "Firstname",
                "lastname": "Lastname",
                "name": "Firstname Lastname",
                "login": "firstname.lastname",
            }
        )

    def create_original_multinames(self):
        self.original_multinames = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "firstname": "Firstname1 Firstname2",
                    "lastname": "Lastname1 Lastname2",
                    "name": "Firstname1 Firstname2 Lastname1 Lastname2 (copy)",
                    "login": "firstname.multi",
                }
            )
        )

    def compare(self, copy):
        self.assertEqual(copy.lastname, "Lastname2")
        self.assertEqual(copy.firstname, "Firstname2")
        self.assertEqual(copy.name, "Firstname2 Lastname2")

    def test_copy_login(self):
        copy = self.original.copy()
        self.assertEqual(copy.login, "firstname.lastname (copy)")

    def test_copy_login_default(self):
        copy = self.original.copy({"login": "login"})
        self.assertEqual(copy.login, "login")

    def test_copy_name(self):
        """Copy original with default name set - firstname lastname not set."""
        copy = self.original.copy({"name": "Firstname2 Lastname2"})
        self.compare(copy)

    def test_copy_firstname_lastname(self):
        """Copy original with default firstname and lastname set"""
        copy = self.original.copy({"firstname": "Firstname2", "lastname": "Lastname2"})
        self.compare(copy)

    def test_copy_firstname_lastname_name(self):
        """Copy original with default firstname, lastname and name set"""
        copy = self.original.copy(
            {
                "firstname": "Firstname2",
                "lastname": "Lastname2",
                "name": "Firstname2 Lastname2",
            }
        )
        self.compare(copy)

    def test_copy_multiple_names(self):
        copy = self.original_multinames.partner_id.copy()
        self.assertRecordValues(
            copy,
            [
                {
                    "firstname": "Firstname1 Firstname2",
                    "lastname": "Lastname1 Lastname2 (copy)",
                    "name": "Firstname1 Firstname2 Lastname1 Lastname2 (copy)",
                }
            ],
        )

    def test_copy_multiple_names_company(self):
        partner = self.original_multinames.partner_id
        partner.is_company = True
        copy = partner.copy()
        self.assertRecordValues(
            copy,
            [
                {
                    "firstname": "Firstname1 Firstname2",
                    "lastname": "Lastname1 Lastname2 (copy)",
                    "name": "Firstname1 Firstname2 Lastname1 Lastname2 (copy)",
                }
            ],
        )

    def test_copy_multiple_partners(self):
        partners = self.env.ref("base.partner_admin") | self.env.ref(
            "base.partner_demo"
        )
        dupes = partners.copy()
        self.assertEqual(len(dupes), 2)

    def test_copy_multiple_users(self):
        users = self.env.ref("base.user_admin") | self.env.ref("base.user_demo")
        dupes = users.copy()
        self.assertEqual(len(dupes), 2)
