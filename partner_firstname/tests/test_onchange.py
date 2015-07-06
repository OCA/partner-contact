# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase


class PartnerCompanyCase(TransactionCase):
    def test_create_from_form(self):
        """A user creates a company from the form."""
        name = u"Sôme company"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is a company
            partner.is_company = True

            # User sets a name, that triggers ``_onchange_name()``
            partner.name = name
            partner._onchange_name()

            self.assertEqual(partner.name, name)
            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, name)


class PartnerContactCase(TransactionCase):
    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = u"Fïrst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is not a company
            partner.is_company = False

            # Changes firstname, which triggers _onchange_name()
            partner.firstname = firstname
            partner._onchange_name()

            self.assertEqual(partner.lastname, False)
            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.name, firstname)

    def test_create_from_form_only_lastname(self):
        """A user creates a contact with only the lastname from the form."""
        lastname = u"Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is not a company
            partner.is_company = False

            # Changes lastname, which triggers _onchange_name()
            partner.lastname = lastname
            partner._onchange_name()

            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.name, lastname)

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = u"Fïrst"
        lastname = u"Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is not a company
            partner.is_company = False

            # Changes firstname, which triggers _onchange_name()
            partner.firstname = firstname
            partner._onchange_name()

            # Changes lastname, which triggers _onchange_name()
            partner.lastname = lastname
            partner._onchange_name()

            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.name, u" ".join(lastname, firstname))
