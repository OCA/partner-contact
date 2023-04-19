# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa

from odoo.tests.common import TransactionCase

from odoo.addons.partner_firstname.tests.base import MailInstalled


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""

    model = "res.partner"
    context = dict()

    def setUp(self):
        super().setUp()
        self.env["ir.config_parameter"].set_param(
            "partner_names_order", "last_first_comma"
        )

        self.firstname = "Fírstname"
        self.middlename = "Middlename"
        self.lastname = "Làstname1"
        self.template = "%(last1)s %(first)s, %(last2)s"

    def tearDown(self):
        try:
            new = self.env[self.model].with_context(**self.context).create(self.params)

            # Check that each individual field matches
            self.assertEqual(self.firstname, new.firstname, "First name saved badly.")
            self.assertEqual(self.lastname, new.lastname, "Last name 1 saved badly.")
            self.assertEqual(
                self.middlename, new.middlename, "Middle name saved badly."
            )

            # Check that name gets saved fine
            self.assertEqual(
                self.template
                % (
                    {
                        "first": self.firstname,
                        "last1": self.lastname,
                        "last2": self.middlename,
                    }
                ),
                new.name,
                "Name saved badly.",
            )

        finally:
            super().tearDown()

    def test_firstname_first(self):
        """Create a person setting his first name first."""
        self.env["ir.config_parameter"].set_param("partner_names_order", "first_last")
        self.template = "%(first)s %(last2)s %(last1)s"
        self.params = {
            "is_company": False,
            "name": "{} {} {}".format(self.firstname, self.middlename, self.lastname),
        }

    def test_firstname_last_wo_comma(self):
        """Create a person setting his first name last and the order as 'last_first'"""
        self.env["ir.config_parameter"].set_param("partner_names_order", "last_first")
        self.template = "%(last1)s %(first)s %(last2)s"
        self.params = {
            "is_company": False,
            "name": "{} {} {}".format(self.lastname, self.middlename, self.firstname),
        }

    def test_firstname_only(self):
        """Create a person setting his first name only."""
        self.env["ir.config_parameter"].set_param("partner_names_order", "first_last")
        self.firstname = self.middlename = False
        self.template = "%(last1)s"
        self.params = {
            "is_company": False,
            "name": self.lastname,
        }

    def test_firstname_lastname_only(self):
        """Create a person setting his first name and last name 1 only."""
        self.env["ir.config_parameter"].set_param("partner_names_order", "first_last")
        self.middlename = False
        self.template = "%(first)s %(last1)s"
        self.params = {
            "is_company": False,
            "name": "{} {}".format(self.firstname, self.lastname),
        }

    def test_lastname_firstname_only_wo_comma(self):
        """Create a person setting his last name 1 and first name only.
        Set order to 'last_first' to test name split without comma"""
        self.env["ir.config_parameter"].set_param("partner_names_order", "last_first")
        self.middlename = False
        self.template = "%(last1)s %(first)s"
        self.params = {
            "is_company": False,
            "name": "{} {}".format(self.lastname, self.firstname),
        }


class UserCase(PersonCase, MailInstalled):
    """Test ``res.users``."""

    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Skip if ``mail`` is installed
        if not self.mail_installed():
            super().tearDown()
