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

        self.original = self.env["res.partner"].create({
            "lastname": "lastname",
            "firstname": "firstname"})

    def test_copy_partner(self):
        """Copy the partner and compare the result."""
        copy = self.original.with_context(lang="en_US").copy()

        self.assertEqual(
            copy.name,
            "lastname firstname (copy)",
            "Copy of the partner failed with wrong name")
        self.assertEqual(
            copy.lastname,
            "lastname",
            "Copy of the partner failed with wrong lastname")
        self.assertEqual(
            copy.firstname,
            "firstname (copy)",
            "Copy of the partner failed with wrong firstname")

    def test_update_user_lastname(self):
        """Change lastname."""
        self.original.name = "changed firstname"

        self.assertEqual(
            self.original.name,
            "changed firstname",
            "Update of the partner lastname failed with wrong name")
        self.assertEqual(
            self.original.lastname,
            "changed",
            "Update of the partner lastname failed with wrong lastname")
        self.assertEqual(
            self.original.firstname,
            "firstname",
            "Update of the partner lastname failed with wrong firstname")

    def test_update_user_firstname(self):
        """Change firstname."""
        self.original.name = "lastname changed"

        self.assertEqual(
            self.original.name,
            "lastname changed",
            "Update of the partner lastname failed with wrong name")
        self.assertEqual(
            self.original.lastname,
            "lastname",
            "Update of the partner lastname failed with wrong lastname")
        self.assertEqual(
            self.original.firstname,
            "changed",
            "Update of the partner lastname failed with wrong firstname")

    def test_no_names(self):
        """Test that you cannot set a partner without names."""
        with self.assertRaises(ex.EmptyNames):
            self.original.firstname = self.original.lastname = False


class UserFirstnameCase(TransactionCase):
    def setUp(self):
        super(UserFirstnameCase, self).setUp()

        self.original = self.env["res.users"].create({
            "name": "lastname firstname",
            "login": "firstnametest@example.com"})

    def test_copy_user(self):
        """Copy the user and compare result."""
        copy = self.original.with_context(lang="en_US").copy()

        self.assertEqual(
            copy.name,
            "lastname firstname (copy)",
            "Copy of the partner failed with wrong name")
        self.assertEqual(
            copy.lastname,
            "lastname",
            "Copy of the partner failed with wrong lastname")
        self.assertEqual(
            copy.firstname,
            "firstname (copy)",
            "Copy of the partner failed with wrong firstname")

    def test_update_user_lastname(self):
        """Change lastname."""
        self.original.name = "changed firstname"

        self.assertEqual(
            self.original.name,
            "changed firstname",
            "Update of the user lastname failed with wrong name")
        self.assertEqual(
            self.original.lastname,
            "changed",
            "Update of the user lastname failed with wrong lastname")
        self.assertEqual(
            self.original.firstname,
            "firstname",
            "Update of the user lastname failed with wrong firstname")

    def test_update_user_firstname(self):
        """Change firstname."""
        self.original.name = "lastname changed"

        self.assertEqual(
            self.original.name,
            "lastname changed",
            "Update of the user lastname failed with wrong name")
        self.assertEqual(
            self.original.lastname,
            "lastname",
            "Update of the user lastname failed with wrong lastname")
        self.assertEqual(
            self.original.firstname,
            "changed",
            "Update of the user lastname failed with wrong firstname")
