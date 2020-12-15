# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class PartnerNamesOrder(TransactionCase):
    def test_get_computed_name(self):
        firstname = "Johan"
        othernames = "Alejandro"
        lastname = "Olano"
        lastname2 = "Ramirez"
        cases = (
            ('last_first', "Olano Ramirez Johan Alejandro "),
            ('last_first_comma', "Olano Ramirez, Johan Alejandro"),
            ('first_last', "Johan Alejandro Olano Ramirez"),
        )

        for name in cases:
            result = self.env['res.partner']._get_computed_name(
                firstname, othernames, lastname, lastname2)
            self.assertEqual(result, name)

    def test_get_inverse_name(self):
        firstname = "Johan"
        othernames = "Alberto"
        lastname = "Marin"
        lastname2 = "Bustamente"
        cases = (
            ('last_first', "Marin Bustamente Johan Alberto"),
            ('last_first_comma', "Marin Bustamante, Johan Alberto"),
            ('first_last', "Johan Alberto Marin Bustamante"),
        )
        for name in cases:
            result = self.env['res.partner']._get_inverse_name(name)
            self.assertEqual(result['firstname'], firstname)
            self.assertEqual(result['othernames'], othernames)
            self.assertEqual(result['lastname'], lastname)
            self.assertEqual(result['lastname2'], lastname2)
