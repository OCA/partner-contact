# -*- coding: utf-8 -*-
# Copyright 2015 Yannick Vaucher, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCompletion(TransactionCase):

    def test_onchange_better_zip_state_id(self):
        """ Test onchange on res.better.zip """
        usa_MA = self.env.ref('base.state_us_34')
        self.better_zip1.state_id = usa_MA
        self.better_zip1.onchange_state_id()
        self.assertEqual(self.better_zip1.country_id, usa_MA.country_id)

    def test_onchange_partner_city_completion(self):
        self.partner1.zip_id = self.better_zip1
        self.partner1.onchange_zip_id()
        self.assertEqual(self.partner1.zip, self.better_zip1.name)
        self.assertEqual(self.partner1.city, self.better_zip1.city)
        self.assertEqual(self.partner1.state_id, self.better_zip1.state_id)
        self.assertEqual(self.partner1.country_id, self.better_zip1.country_id)

    def test_onchange_company_city_completion(self):
        self.company.better_zip_id = self.better_zip1
        self.company.on_change_city()
        self.assertEqual(self.company.zip, self.better_zip1.name)
        self.assertEqual(self.company.city, self.better_zip1.city)
        self.assertEqual(self.company.state_id, self.better_zip1.state_id)
        self.assertEqual(self.company.country_id, self.better_zip1.country_id)

    def setUp(self):
        super(TestCompletion, self).setUp()
        state_vd = self.env['res.country.state'].create({
            'name': 'Vaud',
            'code': 'VD',
            'country_id': self.ref('base.ch'),
        })
        self.company = self.env.ref('base.main_company')
        self.better_zip1 = self.env['res.better.zip'].create({
            'name': 1000,
            'city': 'Lausanne',
            'state_id': state_vd.id,
            'country_id': self.ref('base.ch'),
        })
        self.partner1 = self.env['res.partner'].create({
            'name': 'Camptocamp',
        })
