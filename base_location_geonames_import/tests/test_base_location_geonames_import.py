# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestBaseLocationGeonamesImport(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestBaseLocationGeonamesImport, cls).setUpClass()
        cls.country = cls.env.ref('base.mc')
        cls.wizard = cls.env['better.zip.geonames.import'].create({
            'country_id': cls.country.id,
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
        zip_count = self.env['res.better.zip'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertEqual(zip_count, max_import)
        # Reimport again to see that there's no duplicates
        self.wizard.with_context(max_import=max_import).run_import()
        state_count2 = self.env['res.country.state'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertEqual(state_count, state_count2)
        zip_count = self.env['res.better.zip'].search_count([
            ('country_id', '=', self.country.id)
        ])
        self.assertEqual(zip_count, max_import)

    def test_delete_old_entries(self):
        zip_entry = self.env['res.better.zip'].create({
            'city': 'Test city',
            'country_id': self.country.id,
        })
        self.wizard.run_import()
        self.assertFalse(zip_entry.exists())

    def test_import_title(self):
        self.wizard.letter_case = 'title'
        self.wizard.with_context(max_import=1).run_import()
        zip = self.env['res.better.zip'].search(
            [('country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(zip.city, zip.city.title())

    def test_import_upper(self):
        self.wizard.letter_case = 'upper'
        self.wizard.with_context(max_import=1).run_import()
        zip = self.env['res.better.zip'].search(
            [('country_id', '=', self.country.id)], limit=1
        )
        self.assertEqual(zip.city, zip.city.upper())
