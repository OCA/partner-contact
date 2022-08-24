from psycopg2 import IntegrityError
from odoo.tools import mute_logger


from odoo.tests import common


class TestBaseMunicipality(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.municipality_obj = cls.env["res.country.municipality"]
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.municipality_breda = cls.municipality_obj.create({
            "name": "Breda",
            "code": "0758",
            "state_id": cls.env.ref("base.state_nl_nb").id,
            "country_id": cls.env.ref("base.nl").id
        })

    def test_01_sql_unique_constraint(self):
        """Test that municipality code must be unique by country and state!"""
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(IntegrityError):
                self.municipality_obj.create({
                    "name": "Breda",
                    "code": "0758",
                    "state_id": self.env.ref("base.state_nl_nb").id,
                    "country_id": self.env.ref("base.nl").id
                })

    def test_02_company_address_fields_inverse(self):
        """Test inverse fields from res.company"""
        company = self.env["res.company"].create({"name": "Test"})
        company.municipality_id = self.municipality_breda.id
        company._inverse_municipality_id()
        self.assertEqual(
            company.municipality_id,
            company.partner_id.municipality_id
        )

    def test_03_company_address_fields(self):
        """Test if the partner address fields changes when
        changing the ones from the company"""
        company = self.env["res.company"].create({"name": "Test"})
        self.assertTrue(company.partner_id)
        company.partner_id.write(
            {
                "municipality_id": self.municipality_breda.id,
            }
        )
        company._compute_address()
        self.assertEqual(
            company.municipality_id,
            company.partner_id.municipality_id
        )
