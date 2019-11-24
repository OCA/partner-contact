# -*- coding: utf-8 -*-
# © 2014 Nemry Jonathan (Acsone SA/NV) (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from .. import exceptions as ex


class MailInstalled():
    def mail_installed(self):
        """Check if ``mail`` module is installed.``"""
        return (self.env["ir.module.module"]
                .search([("name", "=", "mail")])
                .state == "installed")


class BaseCase(TransactionCase, MailInstalled):
    def setUp(self):
        super(BaseCase, self).setUp()
        self.check_fields = True
        self.expect("Núñez", "Fernán")
        self.create_original()

    def create_original(self):
        self.original = self.env["res.partner"].create({
            "lastname": self.lastname,
            "firstname": self.firstname})

    def expect(self, lastname, firstname, name=None):
        """Define what is expected in each field when ending."""
        self.lastname = lastname
        self.firstname = firstname
        self.name = name or "%s %s" % (lastname, firstname)

    def tearDown(self):
        if self.check_fields:
            if not hasattr(self, "changed"):
                self.changed = self.original

            for field in ("name", "lastname", "firstname"):
                self.assertEqual(
                    getattr(self.changed, field),
                    getattr(self, field),
                    "Test failed with wrong %s" % field)

        super(BaseCase, self).tearDown()

    def test_copy(self):
        """Copy the partner and compare the result."""
        self.expect(self.lastname, "%s (copy)" % self.firstname)
        self.changed = (self.original.with_context(copy=True, lang="en_US")
                        .copy())

    def test_one_name(self):
        """Test what happens when only one name is given."""
        name = "Mönty"
        self.expect(name, False, name)
        self.original.name = name

    def test_no_names(self):
        """Test that you cannot set a partner/user without names."""
        self.check_fields = False
        with self.assertRaises(ex.EmptyNamesError):
            self.original.firstname = self.original.lastname = False


class OnChangeCase(TransactionCase):
    is_company = False

    def new_partner(self):
        """Create an empty partner. Ensure it is (or not) a company."""
        new = self.env["res.partner"].new()
        new.is_company = self.is_company
        return new
