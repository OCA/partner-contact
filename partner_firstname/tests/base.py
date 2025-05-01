# Copyright 2014 Nemry Jonathan (Acsone SA/NV) (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools

from odoo.tests import TransactionCase

from .. import exceptions as ex


def partner_names_orders(func):
    """Execute test method for each partner_names_order selection."""

    @functools.wraps(func)
    def _orders(self):
        for order, _title in self.env[
            "res.config.settings"
        ]._partner_names_order_selection():
            with self.subTest(order=order), self.env.cr.savepoint() as sp:
                self.env["ir.config_parameter"].set_param("partner_names_order", order)
                func(self)
                sp.rollback()

    return _orders


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

    def test_copy(self):
        """Copy the partner and compare the result."""
        self.expect(f"{self.lastname} (copy)", self.firstname)
        self.changed = self.original.with_context(copy=True, lang="en_US").copy()

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
