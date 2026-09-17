# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import datetime
from collections import namedtuple

from odoo.tests.common import Form, TransactionCase

from odoo.addons.partner_data_vies_populator.models import res_partner

MockViesResultType = namedtuple(
    "MockViesResultType",
    ["countryCode", "vatNumber", "requestDate", "valid", "name", "address"],
)


class TestPartnerCreateByVAT(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.be_country_id = cls.env.ref("base.be").id
        cls.sample_1 = {
            "name": "SA ODOO",
            "address": "Chaussée de Namur 40",
            "zip": "1367",
            "city": "Ramillies",
            "country_code": "BE",
        }

    def setUp(self):
        super().setUp()
        self.patch(
            res_partner,
            "check_vies",
            lambda *args, **kwargs: self._mock_check_vies(*args, **kwargs),
        )

    def _mock_check_vies(self, number, *args):
        if number == "BE0477472701":
            return MockViesResultType(
                **{
                    "countryCode": "BE",
                    "vatNumber": "0477472701",
                    "requestDate": datetime.date(2026, 9, 17),
                    "valid": True,
                    "name": "SA ODOO",
                    "address": "Chaussée de Namur 40\n1367 Ramillies",
                }
            )
        elif number == "NL001172359B01":
            return MockViesResultType(
                **{
                    "countryCode": "NL",
                    "vatNumber": "001172359B01",
                    "requestDate": datetime.date(2026, 9, 17),
                    "valid": True,
                    "name": "JUMBO SUPERMARKTEN B.V.",
                    "address": "\nRIJKSWEG 00015\n5462CE VEGHEL\n",
                }
            )
        elif number == "NL856467534B01":
            return MockViesResultType(
                **{
                    "countryCode": "NL",
                    "vatNumber": "856467534B01",
                    "requestDate": datetime.date(2026, 9, 17),
                    "valid": True,
                    "name": "---",
                    "address": "---",
                }
            )
        else:  # pragma: no cover
            raise Exception(
                "You need to add an entry in _mock_check_vies for %s" % number
            )

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

    def test_empty_fields(self):
        partner = self.partner_model.create(
            {
                "name": "Hunki Enterprises",
                "street": "some street",
                "is_company": True,
            }
        )
        with Form(partner) as partner_form:
            partner_form.vat = "NL856467534B01"
            self.assertEqual(partner_form.name, partner.name)
            self.assertEqual(partner_form.street, partner.street)
