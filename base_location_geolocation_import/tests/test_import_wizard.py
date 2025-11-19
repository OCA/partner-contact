# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestBaseLocationGeonamesImport(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env["res.country"].create(
            {
                "code": "EL",
                "name": "El Dorado",
            }
        )
        cls.wizard = cls.env["city.zip.geonames.import"].create(
            {"country_ids": [(6, 0, [cls.country.id])]}
        )

    def test_import_geolocation(self):
        self.wizard.country_ids = [(6, 0, self.country.ids)]
        parsed_csv = [
            [
                "EL",
                "12345",
                "Secret City",
                " Amazone",
                "AZ",
                "Placer",
                "61",
                "",
                "",
                "38.9829",
                "-121.0944",
                "4",
            ],
            [
                "EL",
                "67890",
                "Hidden Temple",
                " Amazone",
                "AZ",
                "Placer",
                "61",
                "",
                "",
                "38.9115",
                "-121.08",
                "4",
            ],
        ]
        self.wizard._process_csv(parsed_csv, self.country)
        zip_entries = self.env["res.city.zip"].search(
            [("city_id.country_id", "=", self.country.id)]
        )
        for zip_entry in zip_entries:
            if zip_entry.name == "12345":
                self.assertEqual(zip_entry.latitude, 38.9829)
                self.assertEqual(zip_entry.longitude, -121.0944)
                self.assertEqual(zip_entry.city_id.name, "Secret City")
            if zip_entry.name == "67890":
                self.assertEqual(zip_entry.latitude, 38.9115)
                self.assertEqual(zip_entry.longitude, -121.08)
                self.assertEqual(zip_entry.city_id.name, "Hidden Temple")
