# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test copy function for models."""

from odoo.tests import TransactionCase

from .base import MailInstalled, partner_names_orders


class PartnerCase(TransactionCase):
    """Test ``res.partner``."""

    def setUp(self):
        super().setUp()
        self.original = self.env.ref("base.partner_demo")

    def compare(self, copy, *, firstname="Marc2", lastname="Demo2"):
        self.assertEqual(copy.lastname, lastname)
        self.assertEqual(copy.firstname, firstname)
        name = {
            "last_first": f"{lastname} {firstname}",
            "last_first_comma": f"{lastname}, {firstname}",
            "first_last": f"{firstname} {lastname}",
        }[self.env["res.partner"]._get_names_order()]
        self.assertEqual(copy.name, name)

    def test_copy_last_first(self):
        self.env["ir.config_parameter"].set_param("partner_names_order", "last_first")
        copy = self.original.copy()
        self.compare(copy, firstname="Marc (copy)", lastname="Demo")

    def test_copy_last_first_comma(self):
        self.env["ir.config_parameter"].set_param(
            "partner_names_order", "last_first_comma"
        )
        copy = self.original.copy()
        self.compare(copy, firstname="Marc (copy)", lastname="Demo")

    def test_copy_first_last(self):
        self.env["ir.config_parameter"].set_param("partner_names_order", "first_last")
        copy = self.original.copy()
        self.compare(copy, firstname="Marc", lastname="Demo (copy)")

    def test_copy_name(self):
        """Copy original with default name set - firstname lastname not set."""
        copy = self.original.copy({"name": "Marc2 Demo2"})
        self.compare(copy)

    @partner_names_orders
    def test_copy_firstname_lastname(self):
        """Copy original with default firstname and lastname set"""
        copy = self.original.copy({"firstname": "Marc2", "lastname": "Demo2"})
        self.compare(copy)

    def test_copy_firstname_lastname_name(self):
        """Copy original with default firstname, lastname and name set"""
        copy = self.original.copy(
            {
                "firstname": "Marc2",
                "lastname": "Demo2",
                "name": "Marc2 Demo2",
            }
        )
        self.compare(copy)


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
        name = {
            "last_first": "Lastname2 Firstname2",
            "last_first_comma": "Lastname2, Firstname2",
            "first_last": "Firstname2 Lastname2",
        }[self.env["res.partner"]._get_names_order()]
        self.assertEqual(copy.name, name)

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

    @partner_names_orders
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
