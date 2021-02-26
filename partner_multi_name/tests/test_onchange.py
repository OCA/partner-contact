# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa

"""These tests try to mimic the behavior of the UI form.

The form operates in onchange mode, with its limitations.
"""

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
        """Companies never have ``firstname`` nor ``lastname2``."""
        super(PartnerCompanyCase, self).tearDown()
        self.assertEqual(self.partner.firstname, False)
        self.assertEqual(self.partner.lastname2, False)

    def set_name(self, value):
        self.partner.name = value

        # It triggers onchange
        self.partner._onchange_name()

        # Ensure it's properly set
        self.assertEqual(self.partner.name, value)

    def test_create_from_form(self):
        """A user creates a company from the form."""
        name = "Sôme company"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_name(name)

            self.assertEqual(self.partner.lastname, name)

    def test_empty_name_and_subnames(self):
        """If the user empties ``name``, subnames must be ``False``.

        Otherwise, the ``required`` attr will not work as expected.
        """
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_name("Fóo")
            self.set_name("")

            self.assertEqual(self.partner.lastname, False)


class PartnerContactCase(OnChangeCase):
    def set_field(self, field, value):
        # Changes the field
        setattr(self.partner, field, value)

        if field in ("firstname", "lastname", "lastname2"):
            # Trigger onchanges
            self.partner._onchange_subnames()
            self.partner._onchange_name()

            # Check it's set OK
            self.assertEqual(getattr(self.partner, field), value)

    def test_create_from_form_empty(self):
        """A user creates a contact from the form.

        All subfields must be false, or the ``required`` attr will not work as
        expected.
        """
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # Odoo tries to compute the name
            self.partner._compute_name()

            # This is then triggered
            self.partner._onchange_name()

            # Subnames must start as False to make the UI work fine
            self.assertEqual(self.partner.firstname, False)
            self.assertEqual(self.partner.lastname, False)
            self.assertEqual(self.partner.lastname2, False)

            # ``name`` cannot be False, or upstream Odoo will fail
            self.assertEqual(self.partner.name, "")

    def test_create_from_form_only_firstname(self):
        """A user creates a contact with only the firstname from the form."""
        firstname = "Fïrst"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("firstname", firstname)

            self.assertEqual(self.partner.lastname, False)
            self.assertEqual(self.partner.lastname2, False)
            self.assertEqual(self.partner.name, firstname)

    def test_create_from_form_only_lastname(self):
        """A user creates a contact with only the lastname from the form."""
        lastname = "Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("lastname", lastname)

            self.assertEqual(self.partner.firstname, False)
            self.assertEqual(self.partner.lastname2, False)
            self.assertEqual(self.partner.name, lastname)

    def test_create_from_form_only_lastname2(self):
        """A user creates a contact with only the lastname2 from the form."""
        lastname2 = "Läst2"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("lastname2", lastname2)

            self.assertEqual(self.partner.firstname, False)
            self.assertEqual(self.partner.lastname, False)
            self.assertEqual(self.partner.name, lastname2)

    def test_create_from_without_firstname(self):
        """A user creates a contact without firstname from the form."""
        lastname = "Läst"
        lastname2 = "Läst2"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("lastname", lastname)
            self.set_field("lastname2", lastname2)

            self.assertEqual(self.partner.firstname, False)
            self.assertEqual(
                self.partner.name,
                "%s %s" % (lastname, lastname2))

    def test_create_from_without_lastname(self):
        """A user creates a contact without lastname from the form."""
        firstname = "Fïrst"
        lastname2 = "Läst2"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("firstname", firstname)
            self.set_field("lastname2", lastname2)

            self.assertEqual(self.partner.lastname, False)
            self.assertEqual(
                self.partner.name,
                "%s, %s" % (lastname2, firstname))

    def test_create_from_without_lastname2(self):
        """A user creates a contact without lastname2 from the form."""
        firstname = "Fïrst"
        lastname = "Läst"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("firstname", firstname)
            self.set_field("lastname", lastname)

            self.assertEqual(self.partner.lastname2, False)
            self.assertEqual(
                self.partner.name,
                "%s, %s" % (lastname, firstname))

    def test_create_from_form_all(self):
        """A user creates a contact with all names from the form."""
        firstname = "Fïrst"
        lastname = "Läst"
        lastname2 = "Läst2"
        with self.env.do_in_onchange():
            # User presses ``new``
            self.partner = self.new_partner()

            # User changes fields
            self.set_field("firstname", firstname)
            self.set_field("lastname", lastname)
            self.set_field("lastname2", lastname2)

            self.assertEqual(
                self.partner.name,
                "%s %s, %s" % (lastname, lastname2, firstname))
