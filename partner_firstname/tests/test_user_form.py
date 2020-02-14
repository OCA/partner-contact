# Copyright 2016 Yannick Vaucher (Camptocamp SA)
# Copyright 2020 Therp BV - https://therp.nl.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import Form, TransactionCase


class UserOnchangeCase(TransactionCase):
    def test_create_from_form_only_firstname(self):
        """In a new users form, a user set only the firstname."""
        login = "Zoë"
        firstname = "Zoë"
        with self.get_clean_user_form() as user_form:
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
        with self.get_clean_user_form() as user_form:
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
        with self.get_clean_user_form() as user_form:
            user_form.login = login
            # Changes firstname, which triggers onchanges
            user_form.firstname = firstname
            # Changes lastname, which triggers onchanges
            user_form.lastname = lastname

        self.assertEqual(user_form.lastname, lastname)
        self.assertEqual(user_form.firstname, firstname)
        self.assertEqual(user_form.name, " ".join((firstname, lastname)))

    def get_clean_user_form(self):
        """Get form without pseudo_fields.

        This will be needed until Odoo Form does weed out these fields by itself.
        """
        form = Form(self.env["res.users"], view="partner_firstname.view_users_form")
        pseudo_fields = [
            fieldname
            for fieldname in form._view["fields"].keys()
            if fieldname[:11] == "sel_groups_" or fieldname[:9] == "in_group_"
        ]
        for fieldname in pseudo_fields:
            del form._view["fields"][fieldname]
            del form._values[fieldname]
        return form
