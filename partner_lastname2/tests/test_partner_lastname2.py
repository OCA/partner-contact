# -*- encoding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp.tests.common import TransactionCase


class CompanyCase(TransactionCase):
    """Test res.partner when it is a company."""

    def tearDown(self):
        try:
            new = self.env["res.partner"].create({
                "is_company": True,
                "name": self.name,
            })

            # Name should be cleaned of unneeded whitespace
            clean_name = " ".join(self.name.split(None))

            # Check it's saved OK
            self.assertEqual(
                new.name,
                clean_name,
                "Saved company name is wrong.")

            # Check it's saved in the lastname
            self.assertEqual(
                new.lastname,
                clean_name,
                "Company name should be saved in the lastname field.")

            # Check that other fields are empty
            self.assertEqual(
                new.firstname,
                False,
                "Company first name must always be empty.")
            self.assertEqual(
                new.lastname2,
                False,
                "Company last name 2 must always be empty.")

        finally:
            super(CompanyCase, self).tearDown()

    def test_long_name(self):
        """Create a company with a long name."""

        self.name = "Some very long name"

    def test_short_name(self):
        """Create a company with a short name."""

        self.name = "Short"

    def test_whitespace_before(self):
        """Create a company with name prefixed with whitespace."""

        self.name = "  Whitespace before"

    def test_whitespace_after(self):
        """Create a company with name suffixed with whitespace."""

        self.name = "Whitespace after   "

    def test_whitespace_inside(self):
        """Create a company with whitespace inside the name."""

        self.name = "Whitespace   inside"

    def test_whitespace_everywhere(self):
        """Create a company with whitespace everywhere in the name."""

        self.name = "  A  lot  of    whitespace   "


class PersonCase(TransactionCase):
    """Test res.partner when it is a person."""

    model = "res.partner"
    context = dict()

    def setUp(self):
        super(PersonCase, self).setUp()

        self.firstname = "Firstname"
        self.lastname = "Lastname1"
        self.lastname2 = "Lastname2"
        self.template = "%(last1)s %(last2)s, %(first)s"

    def tearDown(self):
        try:
            new = (self.env[self.model].with_context(self.context)
                   .create(self.params))

            # Check that each individual field matches
            self.assertEqual(
                self.firstname,
                new.firstname,
                "First name saved badly.")
            self.assertEqual(
                self.lastname,
                new.lastname,
                "Last name 1 saved badly.")
            self.assertEqual(
                self.lastname2,
                new.lastname2,
                "Last name 2 saved badly.")

            # Check that name gets saved fine
            self.assertEqual(
                self.template % ({"last1": self.lastname,
                                  "last2": self.lastname2,
                                  "first": self.firstname}),
                new.name,
                "Name saved badly.")

        finally:
            super(PersonCase, self).tearDown()

    def test_firstname_first(self):
        """Create a person setting his first name first."""

        self.params = {
            "is_company": False,
            "name": "%s %s %s" % (self.firstname,
                                  self.lastname,
                                  self.lastname2),
        }

    def test_firstname_last(self):
        """Create a persong setting his first name last."""

        self.params = {
            "is_company": False,
            "name": "%s %s, %s" % (self.lastname,
                                   self.lastname2,
                                   self.firstname),
        }

    def test_firstname_only(self):
        """Create a persong setting his first name only."""

        self.lastname = self.lastname2 = False
        self.template = "%(first)s"
        self.params = {
            "is_company": False,
            "name": self.firstname,
        }

    def test_firstname_lastname_only(self):
        """Create a persong setting his first name and last name 1 only."""

        self.lastname2 = False
        self.template = "%(last1)s, %(first)s"
        self.params = {
            "is_company": False,
            "name": "%s %s" % (self.firstname, self.lastname),
        }

    def test_lastname_firstname_only(self):
        """Create a persong setting his last name 1 and first name only."""

        self.lastname2 = False
        self.template = "%(last1)s, %(first)s"
        self.params = {
            "is_company": False,
            "name": "%s, %s" % (self.lastname, self.firstname),
        }

    def test_separately(self):
        """Create a person setting separately all fields."""

        self.params = {
            "is_company": False,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "lastname2": self.lastname2,
        }


class UserCase(PersonCase):
    """Test res.users."""

    model = "res.users"
    context = {"default_login": "user@example.com"}
