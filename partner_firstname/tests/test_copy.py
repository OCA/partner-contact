# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""Test copy function for models."""

from odoo.tests.common import TransactionCase
from .base import MailInstalled


class UserCase(TransactionCase, MailInstalled):
    """Test ``res.users``."""
    model = "res.users"
    context = {"default_login": "user@example.com"}

    def setUp(self):
        super(UserCase, self).setUp()
        self.create_original()

    def create_original(self):
        self.original = self.env["res.users"].create({
            "firstname": u"Firstname",
            "lastname": u"Lastname",
            "name": u"Firstname Lastname",
            "login": u"firstname.lastname"
        })

    def compare(self, copy):
        self.assertEqual(copy.lastname, u"Lastname2")
        self.assertEqual(copy.firstname, u"Firstname2")
        self.assertEqual(copy.name, u"Lastname2 Firstname2")

    def test_copy_name(self):
        """Copy original with default name set - firstname lastname not set."""
        copy = self.original.copy(default={
            "name": u"Lastname2 Firstname2"
        })
        self.compare(copy)

    def test_copy_firstname_lastname(self):
        """Copy original with default firstname and lastname set"""
        copy = self.original.copy(default={
            "firstname": u"Firstname2",
            "lastname": u"Lastname2"
        })
        self.compare(copy)

    def test_copy_firstname_lastname_name(self):
        """Copy original with default firstname, lastname and name set"""
        copy = self.original.copy(default={
            "firstname": u"Firstname2",
            "lastname": u"Lastname2",
            "name": u"Lastname2 Firstname2"
        })
        self.compare(copy)
