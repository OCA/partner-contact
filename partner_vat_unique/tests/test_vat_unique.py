# -*- coding: utf-8 -*-
# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestVatUnique(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestVatUnique, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
            'vat': 'ESA12345674'
        })

    def test_duplicated_vat_creation(self):
        with self.assertRaises(ValidationError):
            self.env['res.partner'].with_context(test_vat=True).create({
                'name': 'Second partner',
                'vat': 'ESA12345674'
            })
