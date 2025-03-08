# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests
import werkzeug
from requests import PreparedRequest, Session

from odoo.tests.common import Form, TransactionCase

_super_send = requests.Session.send


class TestPartnerCreateByVAT(TransactionCase):
    @classmethod
    def _request_handler(cls, s: Session, r: PreparedRequest, /, **kw):
        """
        Override to allow requests to the VIES API
        because odoo17 only permit calls to localhost
        (see https://github.com/odoo/odoo/blob/17.0/odoo/tests/common.py#L279 )
        """
        url = werkzeug.urls.url_parse(r.url)
        if url.host in ("ec.europa.eu",):
            return _super_send(s, r, **kw)
        return super()._request_handler(s=s, r=r, **kw)

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
