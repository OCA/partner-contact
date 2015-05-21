# -*- coding: utf-8 -*-

# Authors: Nemry Jonathan
# Copyright (c) 2014 Acsone SA/NV (http://www.acsone.eu)
# All Rights Reserved
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contact a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from openerp.tests.common import TransactionCase
from .. import exceptions as ex


class PartnerFirstnameCase(TransactionCase):
    def setUp(self):
        super(PartnerFirstnameCase, self).setUp()
        self.check_fields = True
        self.expect(u"Núñez", u"Fernán")
        self.create_original()

    def create_original(self):
        self.original = self.env["res.partner"].create({
            "lastname": self.lastname,
            "firstname": self.firstname})

    def expect(self, lastname, firstname, name=None):
        """Define what is expected in each field when ending."""
        self.lastname = lastname
        self.firstname = firstname
        self.name = name or u"%s %s" % (lastname, firstname)

    def tearDown(self):
        if self.check_fields:
            if not hasattr(self, "changed"):
                self.changed = self.original

            for field in ("name", "lastname", "firstname"):
                self.assertEqual(
                    getattr(self.changed, field),
                    getattr(self, field),
                    "Test failed with wrong %s" % field)

        super(PartnerFirstnameCase, self).tearDown()

    def test_copy(self):
        """Copy the partner and compare the result."""
        self.expect(self.lastname, u"%s (copy)" % self.firstname)
        self.changed = self.original.with_context(lang="en_US").copy()

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

    def test_no_names(self):
        """Test that you cannot set a partner/user without names."""
        self.check_fields = False
        with self.assertRaises(ex.EmptyNamesError):
            self.original.firstname = self.original.lastname = False


class UserFirstnameCase(PartnerFirstnameCase):
    def create_original(self):
        self.original = self.env["res.users"].create({
            "name": u"%s %s" % (self.lastname, self.firstname),
            "login": "firstnametest@example.com"})
