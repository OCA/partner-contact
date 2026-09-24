# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form, common


class TestBaseLocation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CountryState = cls.env["res.country.state"]
        City = cls.env["res.city"]
        CityZip = cls.env["res.city.zip"]
        cls.country_es = cls.env.ref("base.es")
        cls.state_bcn = CountryState.create(
            {"name": "Barcelona", "code": "08", "country_id": cls.country_es.id}
        )
        cls.city_bcn = City.create(
            {
                "name": "Barcelona",
                "state_id": cls.state_bcn.id,
                "country_id": cls.env.ref("base.es").id,
            }
        )
        cls.barcelona = CityZip.create(
            {
                "name": "444",
                "city_id": cls.city_bcn.id,
                "latitude": 38.9829,
                "longitude": -121.0944,
            }
        )

    def test_onchange_partner_city_completion(self):
        """Test that partner data is filled accordingly"""
        partner1 = Form(self.env["res.partner"])
        partner1.zip_id = self.barcelona
        self.assertEqual(partner1.zip, self.barcelona.name)
        self.assertEqual(partner1.city, self.barcelona.city_id.name)
        self.assertEqual(partner1.partner_latitude, self.barcelona.latitude)
        self.assertEqual(partner1.partner_longitude, self.barcelona.longitude)
