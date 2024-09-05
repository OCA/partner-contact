# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import tools
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestResPartnerCompanyType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestResPartnerCompanyType, cls).setUpClass()
        cls.company_type = cls.env.ref(
            "partner_company_type.res_partner_company_type_sa"
        )

        cls.company_type_model = cls.env["res.partner.company.type"]

        cls.country_es = cls.env.ref("base.es")
        cls.country_us = cls.env.ref("base.us")
        cls.state_california = cls.env.ref("base.state_us_5")
        cls.state_colorado = cls.env.ref("base.state_us_6")

        cls.partner_id = cls.env.ref("base.res_partner_2")

        cls.company_type_es = cls.company_type_model.create(
            {
                "name": "Company Type Spain",
                "shortcut": "ESP",
                "country_ids": cls.country_es.ids,
            }
        )

        cls.company_type_us = cls.company_type_model.create(
            {
                "name": "Company Type EEUU",
                "shortcut": "USA",
                "country_ids": cls.country_us.ids,
            }
        )

        cls.company_type_us_ca = cls.company_type_model.create(
            {
                "name": "Company Type EEUU California",
                "shortcut": "CA",
                "country_ids": cls.country_us.ids,
                "state_ids": cls.state_california.ids,
            }
        )
        cls.company_type_us_co = cls.company_type_model.create(
            {
                "name": "Company Type EEUU Colorado",
                "shortcut": "CO",
                "country_ids": cls.country_us.ids,
                "state_ids": cls.state_colorado.ids,
            }
        )

    def test_00_duplicate(self):
        # Test Duplicate Company type

        with self.assertRaises(ValidationError), tools.mute_logger("odoo.sql_db"):
            self.company_type.create(
                dict(name=self.company_type.name, shortcut=self.company_type.shortcut)
            )

    def test_01_partner_company_type_country(self):
        """Test to set up a partner_company_type_id according to the country of the partner_id,
        check that raises an error if they don't match."""

        self.partner_id.write(
            {
                "country_id": self.country_es.id,
                "partner_company_type_id": self.company_type_es.id,
            }
        )
        self.assertEqual(self.partner_id.partner_company_type_id, self.company_type_es)

        with self.assertRaises(UserError):
            self.partner_id.write(
                {
                    "partner_company_type_id": self.company_type_us.id,
                }
            )

    def test_02_partner_company_type_state(self):
        """Test to set up an entity_legal_form_id according to the state of the partner_id,
        check that raises an error if they don't match."""

        self.partner_id.write(
            {
                "country_id": self.country_us.id,
                "state_id": self.state_california.id,
                "partner_company_type_id": self.company_type_us_ca.id,
            }
        )
        self.assertEqual(
            self.partner_id.partner_company_type_id, self.company_type_us_ca
        )

        with self.assertRaises(UserError):
            self.partner_id.write(
                {
                    "partner_company_type_id": self.company_type_us_co.id,
                }
            )
