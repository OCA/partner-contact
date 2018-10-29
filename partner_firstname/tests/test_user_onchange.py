# Copyright 2016 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class UserOnchangeCase(TransactionCase):

    def test_create_from_form_only_firstname(self):
        """In a new users form, a user set only the firstname."""
        firstname = "Zoë"
        with self.env.do_in_onchange():
            # Changes firstname, which triggers onchanges
            self.user.firstname = firstname
            self.user._compute_name()

            self.assertEqual(self.user.lastname, False)
            self.assertEqual(self.user.firstname, firstname)
            self.assertEqual(self.user.name, firstname)

    def test_create_from_form_only_lastname(self):
        """In a new user form, a user set only the lastname."""
        lastname = "Żywioł"
        with self.env.do_in_onchange():
            # Changes lastname, which triggers onchanges
            self.user.lastname = lastname
            self.user._compute_name()

            self.assertEqual(self.user.firstname, False)
            self.assertEqual(self.user.lastname, lastname)
            self.assertEqual(self.user.name, lastname)

    def test_create_from_form_all(self):
        """In a new user form, a user set all names."""
        firstname = "Zoë"
        lastname = "Żywioł"
        with self.env.do_in_onchange():
            # Changes firstname, which triggers onchanges
            self.user.firstname = firstname
            self.user._compute_name()

            # Changes lastname, which triggers onchanges
            self.user.lastname = lastname
            self.user._compute_name()

            self.assertEqual(self.user.lastname, lastname)
            self.assertEqual(self.user.firstname, firstname)
            self.assertEqual(self.user.name, " ".join((firstname, lastname)))

    def setUp(self):
        super(UserOnchangeCase, self).setUp()
        self.user = self.env["res.users"].new()
