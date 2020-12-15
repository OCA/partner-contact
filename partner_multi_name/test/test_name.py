# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 EXA Auto Parts S.A.S Guillermo Montoya <Github@guillermm>
# Copyright 2018 EXA Auto Parts S.A.S Joan Marín <Github@JoanMarin>
# Copyright 2018 EXA Auto Parts S.A.S Juan Ocampo <Github@Capriatto>
# Copyright 2020 EXA Auto Parts S.A.S Alejandro Olano <Github@alejo-code>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class CompanyCase(TransactionCase):
    """Test ``res.partner`` when it is a company."""

    def setUp(self):
        super(CompanyCase, self).setUp()
        self.env['ir.config_parameter'].set_param(
            'partner_names_order', 'first_last')

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
            self.assertEqual(
                new.othernames,
                False,
                "Company last othernames must always be empty.")

        finally:
            super(CompanyCase, self).tearDown()


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""
    model = "res.partner"
    context = dict()

    def setUp(self):
        super(PersonCase, self).setUp()
        self.env['ir.config_parameter'].set_param(
            'partner_names_order', 'last_first_comma')

        self.firstname = "Fírstname"
        self.lastname = "Làstname1"
        self.lastname2 = "Lâstname2"
        self.othernames = "othernames"
        self.template = "%(last1)s, %(last2)s, %(first)s, %(othernames)s"

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

            self.assertEqual(
                self.othernames,
                new.othernames,
                "Last othernames saved badly.")

            # Check that name gets saved fine
            self.assertEqual(
                self.template % ({"last1": self.lastname,
                                  "last2": self.lastname2,
                                  "first": self.firstname,
                                  "othernames": self.othernames}),
                new.name,
                "Name saved badly.")

        finally:
            super(PersonCase, self).tearDown()

    def test_firstname_first(self):
        """Create a person setting his first name first."""
        self.env['ir.config_parameter'].set_param(
            'partner_names_order', 'first_last')
        self.template = "%(last1)s, %(last2)s, %(first)s, %(othernames)s"
        self.params = {
            "is_company": False,
            "name": "%s, %s, %s, %s" % (self.firstname,
                                        self.lastname,
                                        self.lastname2,
                                        self.othernames),
        }

    def test_firstname_last(self):
        """Create a person setting his first name last."""
        self.params = {
            "is_company": False,
            "name": "%s, %s, %s, %s" % (self.lastname,
                                        self.lastname2,
                                        self.firstname,
                                        self.othernames),
        }

    def test_separately(self):
        """Create a person setting separately all fields."""
        self.params = {
            "is_company": False,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "lastname2": self.lastname2,
            "othernames": self.othernames
        }
