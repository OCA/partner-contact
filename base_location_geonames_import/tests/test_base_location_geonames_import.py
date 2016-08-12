# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestBaseLocationGeonamesImport(common.TransactionCase):
    def setUp(self):
        super(TestBaseLocationGeonamesImport, self).setUp()
        self.country = self.env.ref('base.mc')
        self.wizard = self.env['better.zip.geonames.import'].create({
            'country_id': self.country.id,
        })

    def test_import_country(self):
        self.wizard.with_context(max_import=10).run_import()
        state_domain = [
            ('code', '=', '01'),
            ('country_id', '=', self.country.id)
        ]
        states = self.env['res.country.state'].search(state_domain)
        self.assertEqual(len(states), 1)
        zip_domain = [
            ('name', '=', '98000'),
            ('city', '=', 'Jardin Exotique'),
            ('state_id', '=', states[0].id),
            ('country_id', '=', self.country.id),
        ]
        zips = self.env['res.better.zip'].search(zip_domain)
        self.assertEqual(len(zips), 1)
        # Reimport again to see that there's no duplicates
        self.wizard.with_context(max_import=10).run_import()
        states = self.env['res.country.state'].search(state_domain)
        self.assertEqual(len(states), 1)
        zips = self.env['res.better.zip'].search(zip_domain)
        self.assertEqual(len(zips), 1)

    def test_delete_old_entries(self):
        zip_entry = self.env['res.better.zip'].create({
            'city': 'Test city',
            'country_id': self.country.id,
        })
        self.wizard.run_import()
        self.assertFalse(zip_entry.exists())
