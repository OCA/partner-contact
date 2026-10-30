# Copyright 2014 Nemry Jonathan (Acsone SA/NV) (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import TransactionCase


class MailInstalled:
    def mail_installed(self):
        """Check if ``mail`` module is installed.``"""
        return (
            self.env["ir.module.module"].search([("name", "=", "mail")]).state
            == "installed"
        )


class BaseCase(TransactionCase, MailInstalled):
    def setUp(self):
        super().setUp()
        self.check_fields = True
        self.expect("Núñez", "Fernán")
        self.create_original()

    def create_original(self):
        self.original = self.env["res.partner"].create(
            {"firstname": self.firstname, "lastname": self.lastname}
        )

    def expect(self, lastname, firstname, name=None):
        """Define what is expected in each field when ending."""
        self.lastname = lastname
        self.firstname = firstname
        self.name = name or f"{firstname} {lastname}"

    def tearDown(self):
        if self.check_fields:
            if not hasattr(self, "changed"):
                self.changed = self.original

            for field in ("name", "lastname", "firstname"):
                self.assertEqual(
                    self.changed[field],
                    getattr(self, field),
                    f"Test failed with wrong {field}",
                )

        super().tearDown()
