# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestVatUnique(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestVatUnique, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.partner = cls.partner_model.create({
            'name': 'Test partner',
            'vat': 'ESA12345674'
        })

    def test_duplicated_vat_creation(self):
        with self.assertRaises(ValidationError):
            self.partner_model.with_context(test_vat=True).create({
                'name': 'Second partner',
                'vat': 'ESA12345674'
            })
