# Copyright 2016 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class UserOnchangeCase(TransactionCase):
    def test_create_from_form_only_firstname(self):
        """In a new users form, a user set only the firstname."""
        login = "Zoë"
        firstname = "Zoë"
        with Form(
            self.env["res.users"], view="partner_firstname.view_users_form"
        ) as user_form:
            user_form.login = login
            # Changes firstname, which triggers onchanges
            user_form.firstname = firstname

        self.assertEqual(user_form.lastname, False)
        self.assertEqual(user_form.firstname, firstname)
        self.assertEqual(user_form.name, firstname)

    def test_create_from_form_only_lastname(self):
        """In a new user form, a user set only the lastname."""
        login = "Żywioł"
        lastname = "Żywioł"
        with Form(
            self.env["res.users"], view="partner_firstname.view_users_form"
        ) as user_form:
            user_form.login = login
            # Changes lastname, which triggers onchanges
            user_form.lastname = lastname

        self.assertEqual(user_form.firstname, False)
        self.assertEqual(user_form.lastname, lastname)
        self.assertEqual(user_form.name, lastname)

    def test_create_from_form_all(self):
        """In a new user form, a user set all names."""
        login = "Zoë.Żywioł"
        firstname = "Zoë"
        lastname = "Żywioł"
        with Form(
            self.env["res.users"], view="partner_firstname.view_users_form"
        ) as user_form:
            user_form.login = login
            # Changes firstname, which triggers onchanges
            user_form.firstname = firstname

            # Changes lastname, which triggers onchanges
            user_form.lastname = lastname

        self.assertEqual(user_form.lastname, lastname)
        self.assertEqual(user_form.firstname, firstname)
        self.assertEqual(user_form.name, " ".join((firstname, lastname)))
