# -*- coding: utf-8 -*-
# © 2014-2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Test situations where names are empty.

To have more accurate results, remove the ``mail`` module before testing.
"""

from openerp.tests.common import TransactionCase
from .base import MailInstalled
from .. import exceptions as ex


class CompanyCase(TransactionCase):
    """Test ``res.partner`` when it is a company."""
    model = "res.partner"
    context = {"default_is_company": True}

    def tearDown(self):
        try:
            data = {"name": self.name}
            with self.assertRaises(ex.EmptyNamesError):
                self.env[self.model].with_context(**self.context).create(data)
        finally:
            super(CompanyCase, self).tearDown()

    def test_name_empty_string(self):
        """Test what happens when the name is an empty string."""
        self.name = ""

    def test_name_false(self):
        """Test what happens when the name is ``False``."""
        self.name = False


class PersonCase(CompanyCase):
    """Test ``res.partner`` when it is a person."""
    context = {"default_is_company": False}


class UserCase(CompanyCase, MailInstalled):
    """Test ``res.users``."""
    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Cannot create users if ``mail`` is installed
        if self.mail_installed():
            # Skip tests
            super(CompanyCase, self).tearDown()
        else:
            # Run tests
            super(UserCase, self).tearDown()
