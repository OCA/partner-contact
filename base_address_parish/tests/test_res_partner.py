# Copyright 2022: PBox (<https://www.pupilabox.net.ec>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tests.common import Form


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()

    @classmethod
    def setUpClass(cls):
        super(TestResPartner, cls).setUpClass()

        # models
        cls.country_model = cls.env["res.country"]
        cls.states_model = cls.env["res.country.state"]
        cls.cities_model = cls.env["res.city"]

        cls.country = cls.env.ref("base.ec")
        cls.country.write({"enforce_parishes": True, "enforce_cities": True})

        cls.states = cls.env["res.country.state"].search(
            [("country_id", "=", cls.country.id)]  # In Ecuador uses Parishes
        )

        cls.city = cls.env["res.city"].create(
            {
                "name": "CUENCA",
                "country_id": cls.country.id,
                "state_id": cls.states[0].id,
            }
        )

        cls.parish = cls.env["res.parish"].create(
            {"name": "BELLAVISTA", "city_id": cls.city.id, "zip": "010115"},
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
                "vat": "EC1103410021",
                "country_id": cls.country.id,
                "state_id": cls.states[0].id,
                "city_id": cls.city.id,
                "parish_id": cls.parish.id,
                "zip": cls.parish.zip,
            }
        )

        cls.partner_no_parish = cls.env["res.partner"].create(
            {"name": "Test partner no parish"}
        )

    def test_city_creation(self):
        """Test City created"""
        self.assertEqual(self.city.name, "CUENCA")

    def test_parish_creation(self):
        """Test Parish created"""
        self.assertEqual(self.parish.name, "BELLAVISTA")

    def test_parish_name_search(self):
        """Test name search and partner field"""
        names = self.parish.name_search(name="Bella")
        self.assertEqual(self.parish.name, "BELLAVISTA")
        self.assertEqual(names[0][0] == self.parish.id, True)

    def test_partner_parish_creation(self):
        self.assertEqual(self.partner.parish_id.name, "BELLAVISTA")
        self.assertEqual(self.partner.city_id.name, "CUENCA")
        self.assertEqual(self.partner.city_id.name, self.partner.parish_id.city_id.name)
        self.assertEqual(
            self.partner.state_id.name, self.partner.parish_id.state_id.name
        )
        self.assertEqual(self.partner.zip, self.partner.parish_id.zip)

    def test_partner_no_parish_creation(self):
        self.assertEqual(not self.partner_no_parish.parish_id, True)
        self.assertEqual(not self.partner_no_parish.city_id, True)
        self.assertEqual(not self.partner_no_parish.state_id, True)
        self.assertEqual(not self.partner_no_parish.zip, True)

    def test_onchange_partner_parish_completion(self):
        """Test that partner data is filled accodingly"""
        partner1 = Form(self.env["res.partner"])
        partner1.parish_id = self.parish
        self.assertEqual(partner1.city, self.parish.city_id.name)
        self.assertEqual(partner1.state_id, self.parish.state_id)
        self.assertEqual(partner1.country_id, self.parish.country_id)

    def test_onchange_partner_not_parish_completion(self):
        """Test that partner data is filled accodingly"""
        partner1 = Form(self.env["res.partner"])
        self.assertEqual(not partner1.city, True)
        self.assertEqual(not partner1.state_id, True)
        self.assertEqual(not partner1.country_id, True)
