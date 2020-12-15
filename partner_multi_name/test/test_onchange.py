# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class OnChangeCase(TransactionCase):
    is_company = False

    def setUp(self):
        super(OnChangeCase, self).setUp()
        self.env['ir.config_parameter'].set_param(
            'partner_names_order', 'last_first_comma')

    def new_partner(self):
        """Create an empty partner. Ensure it is (or not) a company."""
        new = self.env["res.partner"].new()
        new.is_company = self.is_company
        return new


class PartnerCompanyCase(OnChangeCase):
    is_company = True

    def tearDown(self):
        super(PartnerCompanyCase, self).tearDown()
        self.assertEqual(self.partner.othernames, False)

    def set_name(self, value):
        self.partner.name = value

        # It triggers onchange
        self.partner._onchange_name()

        # Ensure it's properly set
        self.assertEqual(self.partner.name, value)

    def test_create_from_form(self):
        """A user creates a company from the form."""
        name = "Exa Solutions"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_name(name)

            self.assertEqual(self.partner.lastname, name)
