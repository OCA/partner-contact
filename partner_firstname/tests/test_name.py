# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Test naming logic.

To have more accurate results, remove the ``mail`` module before testing.
"""

from .base import BaseCase


class PartnerContactCase(BaseCase):
    def test_update_lastname(self):
        """Change lastname."""
        self.expect(u"newlästname", self.firstname)
        self.original.name = self.name

    def test_update_firstname(self):
        """Change firstname."""
        self.expect(self.lastname, u"newfïrstname")
        self.original.name = self.name

    def test_whitespace_cleanup(self):
        """Check that whitespace in name gets cleared."""
        self.expect(u"newlästname", u"newfïrstname")
        self.original.name = "  newlästname  newfïrstname  "

        # Need this to refresh the ``name`` field
        self.original.invalidate_cache()


class PartnerCompanyCase(BaseCase):
    def create_original(self):
        super(PartnerCompanyCase, self).create_original()
        self.original.is_company = True

    def test_copy(self):
        """Copy the partner and compare the result."""
        super(PartnerCompanyCase, self).test_copy()
        self.expect(self.name, False, self.name)

    def test_company_inverse(self):
        """Test the inverse method in a company record."""
        name = u"Thïs is a Companŷ"
        self.expect(name, False, name)
        self.original.name = name


class UserCase(PartnerContactCase):
    def create_original(self):
        name = u"%s %s" % (self.lastname, self.firstname)

        # Cannot create users if ``mail`` is installed
        if self.mail_installed():
            self.original = self.env.ref("base.user_demo")
            self.original.name = name
        else:
            self.original = self.env["res.users"].create({
                "name": name,
                "login": "firstnametest@example.com"})

    def test_copy(self):
        """Copy the partner and compare the result."""
        # Skip if ``mail`` is installed
        if not self.mail_installed():
            super(UserCase, self).test_copy()
