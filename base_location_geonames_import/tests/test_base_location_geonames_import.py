# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# Copyright 2016-2024 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import requests

from odoo.exceptions import UserError
from odoo.tests import common


class TestBaseLocationGeonamesImport(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        cls._super_send = requests.Session.send
        super().setUpClass()
        cls.country = cls.env.ref("base.mc")
        cls.city = cls.env["res.city"].create(
            {"name": "Test city", "country_id": cls.country.id}
        )
        cls.wizard = cls.env["city.zip.geonames.import"].create(
            {"country_ids": [(6, 0, [cls.country.id])]}
        )
        cls.wrong_country = cls.env["res.country"].create(
            {"name": "Wrong country", "code": "ZZYYXX"}
        )
        cls.wrong_wizard = cls.env["city.zip.geonames.import"].create(
            {"country_ids": [(6, 0, [cls.wrong_country.id])]}
        )
        cls.country_2 = cls.env.ref("base.li")
        cls.country_3 = cls.env.ref("base.sm")
        cls.wizard_2 = cls.env["city.zip.geonames.import"].create(
            {"country_ids": [(6, 0, [cls.country_2.id, cls.country_3.id])]}
        )
        cls.country_4 = cls.env.ref("base.ad")
        cls.wizard_3 = cls.env["city.zip.geonames.import"].create(
            {"country_ids": [(4, cls.country_4.id)]}
        )

    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        """Don't block external requests."""
        return cls._super_send(s, r, **kw)

    def test_import_country(self):
        max_import = 10
        self.wizard.with_context(max_import=max_import).run_import()
        # Look if there are imported states for the country
        state_count = self.env["res.country.state"].search_count(
            [("country_id", "=", self.country.id)]
        )
        self.assertTrue(state_count)
        # Look if there are imported zips
        zip_count = self.env["res.city.zip"].search_count(
            [("city_id.country_id", "=", self.country.id)]
        )
        self.assertEqual(zip_count, max_import)

        # Look if there are imported cities
        city_count = self.env["res.city"].search_count(
            [("country_id", "=", self.country.id)]
        )
        self.assertTrue(city_count)

        # Reimport again to see that there's no duplicates
        self.wizard.with_context(max_import=max_import).run_import()
        state_count2 = self.env["res.country.state"].search_count(
            [("country_id", "=", self.country.id)]
        )
        self.assertEqual(state_count, state_count2)

        city_count2 = self.env["res.city"].search_count(
            [("country_id", "=", self.country.id)]
        )
        self.assertEqual(city_count, city_count2)

        zip_count = self.env["res.city.zip"].search_count(
            [("city_id.country_id", "=", self.country.id)]
        )
        self.assertEqual(zip_count, max_import)

    def test_delete_old_entries(self):
        zip_entry = self.env["res.city.zip"].create(
            {"name": "Brussels", "city_id": self.city.id}
        )
        self.wizard.run_import()
        self.assertFalse(zip_entry.exists())

        city_entry = self.env["res.city"].create(
            {"name": "Test city", "country_id": self.country.id}
        )
        self.wizard.run_import()
        self.assertFalse(city_entry.exists())

    def test_import_title(self):
        self.wizard.letter_case = "title"
        self.wizard.with_context(max_import=1).run_import()
        city_zip = self.env["res.city.zip"].search(
            [("city_id.country_id", "=", self.country.id)], limit=1
        )
        self.assertEqual(city_zip.city_id.name, city_zip.city_id.name.title())

        city = self.env["res.city"].search(
            [("country_id", "=", self.country.id)], limit=1
        )
        self.assertEqual(city.name, city.name.title())

    def test_import_upper(self):
        self.wizard.letter_case = "upper"
        self.wizard.with_context(max_import=1).run_import()
        city_zip = self.env["res.city.zip"].search(
            [("city_id.country_id", "=", self.country.id)], limit=1
        )
        self.assertEqual(city_zip.city_id.name, city_zip.city_id.name.upper())

        city = self.env["res.city"].search(
            [("country_id", "=", self.country.id)], limit=1
        )
        self.assertEqual(city.name, city.name.upper())

    def test_download_error(self):
        """Check that we get an error when trying to download
        with a wrong country code"""
        with self.assertRaises(UserError):
            self.wrong_wizard.run_import()

    def test_import_duplicated_city_name(self):
        country = self.env.ref("base.us")
        self.wizard.country_ids = [(6, 0, country.ids)]
        parsed_csv = [
            [
                "US",
                "95602",
                "Auburn",
                " California",
                "CA",
                "Placer",
                "61",
                "38.9829",
                "-121.0944",
                "4",
            ],
            [
                "US",
                "95603",
                "Auburn",
                " California",
                "CA",
                "Placer",
                "61",
                "38.9115",
                "-121.08",
                "4",
            ],
            [
                "US",
                "30011",
                "Auburn",
                " Georgia",
                "GA",
                "Barrow",
                "13",
                "34.0191",
                "-83.8261",
                "4",
            ],
        ]
        self.wizard._process_csv(parsed_csv, country)
        cities = self.env["res.city"].search([("name", "=", "Auburn")])
        self.assertEqual(len(cities), 2)
        mapping = [
            ["California", "95602"],
            ["California", "95603"],
            ["Georgia", "30011"],
        ]
        for state_name, zip_code in mapping:
            zip_entry = self.env["res.city.zip"].search(
                [("city_id.country_id", "=", country.id), ("name", "=", zip_code)]
            )
            state = self.env["res.country.state"].search(
                [("country_id", "=", country.id), ("name", "=", state_name)]
            )
            self.assertEqual(
                zip_entry.city_id.state_id,
                state,
                f"Incorrect state for {state_name} {zip_code}",
            )

    def test_import_countries(self):
        max_import = 1
        self.wizard_2.with_context(max_import=max_import).run_import()

        # Look if there are imported zips
        zip_country_2_count = self.env["res.city.zip"].search_count(
            [("city_id.country_id", "=", self.country_2.id)]
        )
        zip_country_3_count = self.env["res.city.zip"].search_count(
            [("city_id.country_id", "=", self.country_3.id)]
        )
        self.assertEqual(zip_country_2_count, max_import)
        self.assertEqual(zip_country_3_count, max_import)
