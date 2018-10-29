# Copyright 2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, with its limitations.
"""

from .base import OnChangeCase


class PartnerCompanyCase(OnChangeCase):
    is_company = True

    def test_create_from_form(self):
        """A user creates a company from the form."""
        name = "Sôme company"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

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
            partner = self.new_partner()

            # User sets a name, which triggers onchanges
            partner.name = "Foó"
            partner._onchange_name()

            # User unsets name, which triggers onchanges
            partner.name = ""
            partner._onchange_name()

            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, False)


class PartnerContactCase(OnChangeCase):
    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = "Fïrst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

            # Changes firstname, which triggers onchanges
            partner.firstname = firstname
            partner._onchange_subnames()
            partner._onchange_name()

            self.assertEqual(partner.lastname, False)
            self.assertEqual(partner.firstname, firstname)
            self.assertEqual(partner.name, firstname)

    def test_create_from_form_only_lastname(self):
        """A user creates a contact with only the lastname from the form."""
        lastname = "Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

            # Changes lastname, which triggers onchanges
            partner.lastname = lastname
            partner._onchange_subnames()
            partner._onchange_name()

            self.assertEqual(partner.firstname, False)
            self.assertEqual(partner.lastname, lastname)
            self.assertEqual(partner.name, lastname)

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = "Fïrst"
        lastname = "Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            partner = self.new_partner()

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
            self.assertEqual(partner.name, " ".join((firstname, lastname)))
