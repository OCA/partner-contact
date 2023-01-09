# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, SavepointCase


class TestPartnerCreateByVAT(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.be_country_id = cls.env.ref("base.be").id
        cls.sample_1 = {
            "name": "SA ODOO",
            "address": "Chaussée De Namur 40 1367 Ramillies",
            "country_code": "BE",
        }

    def test_create_from_vat1(self):
        # Create a partner from VAT number field
        with Form(self.partner_model) as partner_form:
            partner_form.is_company = True
            partner_form.vat = "be0477472701"

            # Check if the datas fetch correspond with the datas from VIES.
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(
                partner_form.country_id.code, self.sample_1["country_code"]
            )
            self.assertEqual(partner_form.vat, "BE0477472701")

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
