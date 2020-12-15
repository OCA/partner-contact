# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class UserOnchangeCase(TransactionCase):

    def test_create_from_form_only_firstname(self):
        """In a new users form, a user set only the firstname."""
        firstname = "Alejandro"
        with self.env.do_in_onchange():
            # Changes firstname, which triggers onchanges
            self.user.firstname = firstname
            self.user._compute_name()

            self.assertEqual(self.user.lastname, False)
            self.assertEqual(self.user.othernames, False)
            self.assertEqual(self.user.lastname2, False)
            self.assertEqual(self.user.firstname, firstname)
            self.assertEqual(self.user.name, firstname)

    def test_create_from_form_only_lastname(self):
        """In a new user form, a user set only the lastname."""
        lastname = "Olano"
        with self.env.do_in_onchange():
            # Changes lastname, which triggers onchanges
            self.user.lastname = lastname
            self.user._compute_name()

            self.assertEqual(self.user.firstname, False)
            self.assertEqual(self.user.othernames, False)
            self.assertEqual(self.user.lastname, lastname)
            self.assertEqual(self.user.lastname2, lastname)
            self.assertEqual(self.user.name, lastname)

    def test_create_from_form_all(self):
        """In a new user form, a user set all names."""
        firstname = "Johan"
        othernames = "Alejandro"
        lastname = "Olano"
        lastname2 = "Ramirez"
        with self.env.do_in_onchange():
            # Changes firstname, which triggers onchanges
            self.user.firstname = firstname
            self.user._compute_name()

            # Changes othernames, which triggers onchanges
            self.user.othernames = othernames
            self.user._compute_name()

            # Changes lastname, which triggers onchanges
            self.user.lastname = lastname
            self.user._compute_name()

            # Changes lastname2, which triggers onchanges
            self.user.lastname2 = lastname2
            self.user._compute_name()

            self.assertEqual(self.user.lastname, lastname)
            self.assertEqual(self.user.othernames, othernames)
            self.assertEqual(self.user.firstname, firstname)
            self.assertEqual(self.user.lastname2, lastname2)
            self.assertEqual(self.user.name, " ".join(
                (lastname, othernames, firstname, lastname2)))

    def setUp(self):
        super(UserOnchangeCase, self).setUp()
        self.user = self.env["res.users"].new()
