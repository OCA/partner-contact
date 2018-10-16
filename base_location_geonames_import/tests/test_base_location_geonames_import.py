# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import UserError


class TestBaseLocationGeonamesImport(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref('base.mc')
        cls.city = cls.env['res.city'].create({
            'name': 'Test city',
            'country_id': cls.country.id,
        })
        cls.wizard = cls.env['city.zip.geonames.import'].create({
            'country_id': cls.country.id,
        })
        cls.wrong_country = cls.env['res.country'].create({
            'name': 'Wrong country',
            'code': 'ZZYYXX',
        })
        cls.wrong_wizard = cls.env['city.zip.geonames.import'].create({
            'country_id': cls.wrong_country.id,
        })

    def test_import_country(self):
        max_import = 10
        self.wizard.with_context(max_import=max_import).run_import()
        # Look if there are imported states for the country
        state_count = self.env['res.country.state'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertTrue(state_count)
        # Look if there are imported zips
        zip_count = self.env['res.city.zip'].search_count([
            ('city_id.country_id', '=', self.country.id)
        ])
        self.assertEqual(zip_count, max_import)

        # Look if there are imported cities
        city_count = self.env['res.city'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertTrue(city_count)

        # Reimport again to see that there's no duplicates
        self.wizard.with_context(max_import=max_import).run_import()
        state_count2 = self.env['res.country.state'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertEqual(state_count, state_count2)

        city_count2 = self.env['res.city'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertEqual(city_count, city_count2)

        zip_count = self.env['res.city.zip'].search_count([
            ('city_id.country_id', '=', self.country.id)
        ])
        self.assertEqual(zip_count, max_import)

    def test_delete_old_entries(self):
        zip_entry = self.env['res.city.zip'].create({
            'name': 'Brussels',
            'city_id': self.city.id,
        })
        self.wizard.run_import()
        self.assertFalse(zip_entry.exists())

        city_entry = self.env['res.city'].create({
            'name': 'Test city',
            'country_id': self.country.id,
        })
        self.wizard.run_import()
        self.assertFalse(city_entry.exists())

    def test_import_title(self):
        self.wizard.letter_case = 'title'
        self.wizard.with_context(max_import=1).run_import()
        zip = self.env['res.city.zip'].search(
            [('city_id.country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(zip.city_id.name, zip.city_id.name.title())

        city = self.env['res.city'].search(
            [('country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(city.name, city.name.title())

    def test_import_upper(self):
        self.wizard.letter_case = 'upper'
        self.wizard.with_context(max_import=1).run_import()
        zip = self.env['res.city.zip'].search(
            [('city_id.country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(zip.city_id.name, zip.city_id.name.upper())

        city = self.env['res.city'].search(
            [('country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(city.name, city.name.upper())

    def test_download_error(self):
        """Check that we get an error when trying to download
        with a wrong country code"""
        with self.assertRaises(UserError):
            self.wrong_wizard.run_import()
