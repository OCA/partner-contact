# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, TransactionCase


class TestPartnerCreateByVAT(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner_model = self.env["res.partner"]
        self.sample_1 = {
            "valid": True,
            "name": u"SA ODOO",
            "address": u"Chaussée De Namur 40 1367 Ramillies",
        }

    def test_create_from_vat1(self):
        # Create an partner from VAT number field
        with Form(self.env["res.partner"]) as partner_form:
            partner_form.is_company = True
            partner_form.vat = "be0477472701"

            # Check if the datas fetch correspond with the datas from VIES.
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(partner_form.country_id.name, "Belgium")
            self.assertEqual(partner_form.vat, "BE0477472701")

    def test_vat_change1(self):
        # Change partner VAT number field
        partner1 = self.partner_model.create({"name": "1", "is_company": True})
        with Form(partner1) as partner_form:
            # Check if the datas fetch correspond with the datas from VIES.
            partner_form.vat = "be0477472701"
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(partner_form.country_id.name, "Belgium")
            self.assertEqual(partner_form.vat, "BE0477472701")

            # Empty VAT
            partner_form.vat = False
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(partner_form.country_id.name, "Belgium")

            # Not company
            partner_form.is_company = False
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(partner_form.country_id.name, "Belgium")

            # Not EU country
            partner_form.vat = "GT1234567 - 1"
            self.assertEqual(partner_form.name, self.sample_1["name"])
            self.assertEqual(partner_form.street, self.sample_1["address"])
            self.assertEqual(partner_form.country_id.name, "Belgium")
