# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re
from unittest.mock import MagicMock, patch

import isodate

from odoo.tests import Form, TransactionCase

_original_parse_date = isodate.parse_date


def _patched_parse_date(datestring):
    if isinstance(datestring, str) and re.match(
        r"^\d{4}-\d{2}-\d{2}[+-]\d{2}:?\d{2}$", datestring
    ):
        datestring = datestring[:10]
    return _original_parse_date(datestring)


def mocked_check_vies(vat):
    # Some versions of stdnum might expect a string, others might return an object
    # We simulate a successful response for known test VATs
    vat = str(vat).upper().replace(" ", "")
    res = MagicMock()
    res.valid = True
    if vat == "BE0477472701":
        res.name = "SA ODOO"
        res.address = "Chaussée de Namur 40\n1367 Ramillies"
        res.countryCode = "BE"
    elif vat == "NL001172359B01":
        res.name = "JUMBO SUPERMARKTEN B.V."
        res.address = "RIJKSWEG 00015\n5462CE VEGHEL"
        res.countryCode = "NL"
    else:
        # Default for other VATs to avoid hitting the real service
        res.valid = False
        res.name = "---"
        res.address = "---"
        res.countryCode = vat[:2] if len(vat) > 2 else ""
    return res


class TestPartnerCreateByVAT(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        isodate.parse_date = _patched_parse_date
        # Patch check_vies where it is imported in the model
        cls.patcher = patch(
            "odoo.addons.partner_data_vies_populator.models.res_partner.check_vies",
            side_effect=mocked_check_vies,
        )
        cls.patcher.start()
        # Context needed for compatibility with
        # partner_country_state_required.
        cls.partner_model = cls.env["res.partner"].with_context(no_state_required=True)
        cls.be_country_id = cls.env.ref("base.be").id
        cls.sample_1 = {
            "name": "SA ODOO",
            "address": "Chaussée de Namur 40",
            "zip": "1367",
            "city": "Ramillies",
            "country_code": "BE",
        }

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        isodate.parse_date = _original_parse_date
        super().tearDownClass()

    def test_create_from_vat1(self):
        # Create an partner from VAT number field
        with Form(self.partner_model) as partner_form:
            partner_form.company_type = "company"
            partner_form.vat = "be0477472701"
            # Check if the datas fetch correspond with the datas from VIES.
            # address: 'Chaussée de Namur 40\n1367 Ramillies'
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(
                partner_form.country_id.code, self.sample_1["country_code"]
            )
            self.assertEqual(partner_form.vat, "BE0477472701")

    def test_create_from_vat2nl(self):
        # Create an partner from VAT number field
        with Form(self.partner_model) as partner_form:
            partner_form.company_type = "company"
            partner_form.vat = "NL001172359B01"
            # Check if the datas fetch correspond with the datas from VIES.
            # address: '\nRIJKSWEG 00015\n5462CE VEGHEL\n'
            self.assertEqual(partner_form.name, "JUMBO SUPERMARKTEN B.V.")
            self.assertEqual(partner_form.country_id.code, "NL")
            self.assertEqual(partner_form.zip, "5462CE")
            self.assertEqual(partner_form.vat, "NL001172359B01")

    def test_company_vat_change(self):
        # Change partner VAT number field
        partner = self.partner_model.create({"name": "SA ODOO", "is_company": True})
        with Form(partner) as partner_form:
            # Check if the datas fetch correspond with the datas from VIES.
            partner_form.vat = "be0477472701"
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(
                partner_form.country_id.code, self.sample_1["country_code"]
            )
            self.assertEqual(partner_form.vat, "BE0477472701")

    def test_empty_vat_change(self):
        partner = self.partner_model.create(
            {
                "name": "2",
                "is_company": True,
                "country_id": self.be_country_id,
            }
        )
        with Form(partner) as partner_form:
            partner_form.vat = False
            self.assertEqual(partner_form.name, partner.name)
            self.assertEqual(partner_form.street, False)
            self.assertEqual(partner_form.country_id.id, partner.country_id.id)

    def test_individual_vat_change(self):
        partner = self.partner_model.create(
            {
                "name": "3",
                "is_company": False,
                "country_id": self.be_country_id,
            }
        )
        with Form(partner) as partner_form:
            partner_form.vat = "BE0477472701"
            self.assertEqual(partner_form.name, partner.name)
            self.assertEqual(partner_form.street, False)
            self.assertEqual(partner_form.country_id.id, partner.country_id.id)

    def test_non_eu_vat_change(self):
        non_eu_country_id = self.env.ref("base.sc").id
        partner = self.partner_model.create(
            {
                "name": "4",
                "is_company": True,
                "country_id": non_eu_country_id,
            }
        )
        with Form(partner) as partner_form:
            partner_form.vat = "GT1234567 - 1"
            self.assertEqual(partner_form.name, partner.name)
