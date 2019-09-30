# Copyright 2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, with its limitations.
"""

from .base import OnChangeCase
from odoo.tests.common import Form


class PartnerCompanyCase(OnChangeCase):
    is_company = True

    def test_create_from_form(self):
        name = "Sôme company"
        with Form(self.env['res.partner']) as partner_form:
            partner_form.is_company = self.is_company
            partner_form.name = name

        self.assertEqual(partner_form.name, name)
        self.assertEqual(partner_form.firstname, False)
        self.assertEqual(partner_form.lastname, name)

    def test_empty_name_and_subnames(self):
        """If the user empties ``name``, subnames must be ``False``.

        Otherwise, the ``required`` attr will not work as expected.
        """
        with Form(self.env['res.partner']) as partner_form:
            partner_form.is_company = self.is_company

            name = "Foó"
            # User sets a name, which triggers onchanges
            partner_form.name = name
            partner_form.save()
            self.assertEqual(partner_form.name, name)
            self.assertEqual(partner_form.firstname, False)
            self.assertEqual(partner_form.lastname, name)

            # User unsets name, which triggers onchanges
            partner_form.name = ""
            self.assertEqual(partner_form.name, "")
            self.assertEqual(partner_form.firstname, False)
            self.assertEqual(partner_form.lastname, False)

            partner_form.name = name
            partner_form.save()
            self.assertEqual(partner_form.name, name)
            self.assertEqual(partner_form.firstname, False)
            self.assertEqual(partner_form.lastname, name)


class PartnerContactCase(OnChangeCase):
    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = "Fïrst"
        with Form(self.env['res.partner']) as partner_form:
            partner_form.is_company = self.is_company

            # Changes firstname, which triggers onchanges
            partner_form.firstname = firstname

        self.assertEqual(partner_form.lastname, False)
        self.assertEqual(partner_form.firstname, firstname)
        self.assertEqual(partner_form.name, firstname)

    def test_create_from_form_only_lastname(self):
        """A user creates a contact with only the lastname from the form."""
        lastname = "Läst"
        with Form(self.env['res.partner']) as partner_form:
            partner_form.is_company = self.is_company

            # Changes lastname, which triggers onchanges
            partner_form.lastname = lastname

        self.assertEqual(partner_form.firstname, False)
        self.assertEqual(partner_form.lastname, lastname)
        self.assertEqual(partner_form.name, lastname)

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = "Fïrst"
        lastname = "Läst"
        with Form(self.env['res.partner']) as partner_form:
            partner_form.is_company = self.is_company

            # Changes firstname, which triggers onchanges
            partner_form.firstname = firstname

            # Changes lastname, which triggers onchanges
            partner_form.lastname = lastname

        self.assertEqual(partner_form.lastname, lastname)
        self.assertEqual(partner_form.firstname, firstname)
        self.assertEqual(partner_form.name, " ".join((firstname, lastname)))
