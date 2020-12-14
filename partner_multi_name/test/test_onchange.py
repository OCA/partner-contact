# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from .base import OnChangeCase


class PartnerContactCase(OnChangeCase):
    def test_create_from_form_only_firstname_and_lastname(self):
        """A user creates a contact with only the firstname and lastname from the form."""
        firstname = "Alejandro"
        lastname = "Olano"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

            # Changes firstname, lastname which triggers onchanges
            partner.firstname = firstname
            partner.lastname = lastname
            partner._onchange_subnames()

            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.othernames, False)
            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.lastname2, False)
            self.assertEqual(partner.name, " ".join((firstname, lastname)))

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = "Johan"
        othernames = "Alejandro"
        lastname = "Olano"
        lastname2 = "Ramirez"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

            # Changes firstname, which triggers onchanges
            partner.firstname = firstname
            partner._onchange_subnames()

            # Changes othernames, which triggers onchanges
            partner.othernames = othernames
            partner._onchange_subnames()

            # Changes lastname, which triggers onchanges
            partner.lastname = lastname
            partner._onchange_subnames()

            # Changes lastname2, which triggers onchanges
            partner.lastname2 = lastname2
            partner._onchange_subnames()

            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.othernames, othernames)
            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.lastname2, lastname2)
            self.assertEqual(
                partner.name, " ".join(
                    (firstname, othernames, lastname, lastname2)))
