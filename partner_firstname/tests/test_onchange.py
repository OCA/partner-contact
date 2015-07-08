# -*- coding: utf-8 -*-
"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, and has only some limitations that must be
met.
"""

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

            # User sets a name, which triggers onchanges
            partner.name = name
            partner._onchange_name()

            self.assertEqual(partner.name, name)
            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, name)

    def test_empty_name_and_subnames(self):
        """If the user empties ``name``, subnames must be ``False``.

        Otherwise, the ``required`` attr will not work as expected.
        """
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is a company
            partner.is_company = True

            # User sets a name, which triggers onchanges
            partner.name = u"Foó"
            partner._onchange_name()

            # User unsets name, which triggers onchanges
            partner.name = u""
            partner._onchange_name()

            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, False)


class PartnerContactCase(TransactionCase):
    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = u"Fïrst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.env["res.partner"].create({})

            # User ensures it is not a company
            partner.is_company = False

            # Changes firstname, which triggers onchanges
            partner.firstname = firstname
            partner._onchange_subnames()
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

            # Changes lastname, which triggers onchanges
            partner.lastname = lastname
            partner._onchange_subnames()
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

            # Changes firstname, which triggers onchanges
            partner.firstname = firstname
            partner._onchange_subnames()
            partner._onchange_name()

            # Changes lastname, which triggers onchanges
            partner.lastname = lastname
            partner._onchange_subnames()
            partner._onchange_name()

            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.name, u" ".join((lastname, firstname)))
