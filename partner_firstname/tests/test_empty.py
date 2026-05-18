# Copyright 2014-2015 Grupo ESOC <www.grupoesoc.es>
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test situations where names are empty.

To have more accurate results, remove the ``mail`` module before testing.
"""

from odoo.tests import TransactionCase

from .. import exceptions as ex
from .base import MailInstalled


class CompanyCase(TransactionCase):
    """Test ``res.partner`` when it is a company."""

    model = "res.partner"
    context = {"default_is_company": True}

    def tearDown(self):
        try:
            data = {"name": self.name}
            model = self.env[self.model].with_context(**self.context)
            with self.assertRaises(ex.EmptyNamesError):
                model.create(data)
        finally:
            super().tearDown()

    def test_name_empty_string(self):
        """Test what happens when the name is an empty string."""
        self.name = ""

    def test_name_false(self):
        """Test what happens when the name is ``False``."""
        self.name = False


class PersonCase(CompanyCase):
    """Test ``res.partner`` when it is a person."""

    context = {"default_is_company": False, "default_type": "contact"}


class UserCase(CompanyCase, MailInstalled):
    """Test ``res.users``."""

    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Cannot create users if ``mail`` is installed
        if self.mail_installed():
            # Skip tests
            super().tearDown()
        else:
            # Run tests
            super().tearDown()


class AddressCase(TransactionCase):
    """Test ``res.partner`` when it is a address."""

    def test_new_empty_invoice_address(self):
        """Create an invoice patner without name."""
        self.original = self.env["res.partner"].create(
            {"is_company": False, "type": "invoice", "lastname": "", "firstname": ""}
        )

    def test_new_empty_shipping_address(self):
        """Create an shipping patner without name."""
        self.original = self.env["res.partner"].create(
            {"is_company": False, "type": "delivery", "lastname": "", "firstname": ""}
        )


class EmptyNameWithEmailCase(TransactionCase):
    """A partner created with an empty name but an email uses the email.

    The inverse split returns no name parts when ``name`` is empty. When an
    email is available, the email becomes the lastname. Records with neither
    name nor email keep raising ``EmptyNamesError``.
    """

    def test_create_empty_name_with_email(self):
        """Empty ``name`` plus an ``email`` falls back to the email."""
        partner = self.env["res.partner"].create(
            {"type": "contact", "name": "", "email": "only.email@example.com"}
        )
        self.assertTrue(partner.exists())
        self.assertEqual(partner.lastname, "only.email@example.com")

    def test_create_empty_name_no_email(self):
        """Empty ``name`` and no ``email`` still raises."""
        with self.assertRaises(ex.EmptyNamesError):
            self.env["res.partner"].create({"type": "contact", "name": ""})

    def test_name_create_bare_email(self):
        """``name_create`` with a bare email uses the email (regression)."""
        partner_id, _display = self.env["res.partner"].name_create("user@example.com")
        partner = self.env["res.partner"].browse(partner_id)
        self.assertEqual(partner.email, "user@example.com")
        self.assertEqual(partner.lastname, "user@example.com")

    def test_name_create_formatted_email(self):
        """``name_create`` with ``Name <email>`` keeps the split (regression)."""
        partner_id, _display = self.env["res.partner"].name_create(
            "Mario Rossi <mario.rossi@example.com>"
        )
        partner = self.env["res.partner"].browse(partner_id)
        self.assertEqual(partner.email, "mario.rossi@example.com")
        self.assertEqual(partner.firstname, "Mario")
        self.assertEqual(partner.lastname, "Rossi")
