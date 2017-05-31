# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import UserError


class TestBaseLocationNuts(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestBaseLocationNuts, cls).setUpClass()
        cls.importer = cls.env['nuts.import']
        cls.importer.run_import()  # loads nuts
        cls.country_1 = cls.env['res.country'].search([('code', '=', 'ES')])
        cls.country_2 = cls.env['res.country'].search([('code', '=', 'PT')])
        cls.nuts1_2 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'PT')])
        cls.nuts2_1 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'ES2')])
        cls.nuts3_1 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'ES24')])
        cls.nuts4_1 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'ES243')])
        cls.nuts4_2 = cls.env[
            'res.partner.nuts'].search([('code', '=', 'ES300')])
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
            'country_id': cls.country_1.id,
        })
        cls.state_1 = cls.env['res.country.state'].create({
            'name': 'Zaragoza Test',
            'code': 'ZT',
            'country_id': cls.country_1.id,
        })
        cls.nuts4_1.state_id = cls.state_1
        cls.state_2 = cls.env['res.country.state'].create({
            'name': 'Madrid Test',
            'code': 'MT',
            'country_id': cls.country_1.id,
        })
        cls.nuts4_2.state_id = cls.state_2
        cls.country_1.state_level = 4

    def test_onchange_nuts_country(self):
        self.partner.nuts1_id = self.nuts1_2
        self.partner._onchange_nuts1_id()
        self.assertEqual(self.partner.country_id, self.nuts1_2.country_id)

    def test_onchange_nuts(self):
        self.partner.country_id = self.country_2
        self.partner._onchange_country_id()
        self.assertEqual(self.partner.nuts1_id.country_id,
                         self.partner.country_id)
        self.partner.nuts4_id = self.nuts4_1
        self.partner._onchange_nuts4_id()
        self.assertEqual(self.partner.country_id,
                         self.country_1)
        self.assertEqual(self.partner.nuts3_id, self.nuts3_1)
        self.partner._onchange_nuts3_id()
        self.assertEqual(self.partner.nuts2_id, self.nuts2_1)
        self.partner._onchange_nuts2_id()
        self.assertEqual(self.partner.nuts1_id.country_id, self.country_1)
        self.partner.country_id = self.country_2
        self.partner._onchange_country_id()
        self.assertEqual(self.partner.country_id, self.nuts1_2.country_id)
        self.assertFalse(self.partner.nuts2_id)
        self.assertFalse(self.partner.nuts3_id)
        self.assertFalse(self.partner.nuts4_id)

    def test_onchange_states(self):
        self.partner.state_id = self.state_2
        self.partner.onchange_state_id_base_location_nuts()
        self.assertEqual(self.state_2, self.partner.nuts4_id.state_id)
        self.partner.state_id = self.state_1
        self.partner.onchange_state_id_base_location_nuts()
        self.assertEqual(self.state_1, self.partner.nuts4_id.state_id)
        self.partner._onchange_nuts4_id()
        self.assertEqual(self.partner.nuts3_id, self.nuts3_1)
        self.partner._onchange_nuts3_id()
        self.assertEqual(self.partner.nuts2_id, self.nuts2_1)
        self.partner._onchange_nuts2_id()
        self.assertEqual(self.partner.nuts1_id.country_id, self.country_1)

    def test_download_exceptions(self):
        """ Tests download exceptions """
        with self.assertRaises(UserError):
            self.importer._download_nuts(url_base='htttt://test.com')
        with self.assertRaises(UserError):
            self.importer._download_nuts(url_base='http://ec.europa.eu/_404')
