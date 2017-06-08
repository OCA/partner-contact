# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de servicios, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.addons.base_vat.base_vat import _ref_vat
from openerp import exceptions as ex


class CommonCase(TransactionCase):
    """Test common cases, independent to the country of the VAT code."""
    def setUp(self):
        super(CommonCase, self).setUp()

        self.partner = self.env["res.partner"].create({
            "name": __file__,
            "is_company": False,
        })

    def test_empty(self):
        """Remove a VAT from a contact."""
        # First, set a good VAT to have no errors
        self.partner.contact_vat = "ES00000001R"

        # Then remove it
        self.partner.contact_vat = False

        # Nothing special should happen
        self.assertEqual(self.partner.contact_vat, False)

    def test_company_to_partner(self):
        """Set a wrong contact VAT to a company and convert it to person."""
        self.partner.is_company = True

        # Set a wrong contact_vat, but no errors because it is a company
        self.partner.contact_vat = "ES00000001W"

        # Now say it's a person
        with self.assertRaises(ex.ValidationError):
            self.partner.is_company = False

    def test_vat_without_country_code(self):
        """Set a VAT without the country code prefix."""
        with self.assertRaises(ex.ValidationError):
            self.partner.contact_vat = "00000001R"

    def test_wrong_format_hint(self):
        """Ensure the format hint is given to user."""
        try:
            # Set a wrong VAT
            self.partner.with_context(lang="en_US").contact_vat = "ES00000001W"
        except ex.ValidationError as error:
            self.assertIn(_ref_vat.get("es"), error.value)
            self.assertEqual(error.value, error.args[1])
