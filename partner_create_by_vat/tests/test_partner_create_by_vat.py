# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import mock
from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError

mock_vies = 'openerp.addons.partner_create_by_vat.' \
            'models.res_partner.check_vies'


class TestPartnerCreatebyVAT(TransactionCase):

    def setUp(self):
        super(TestPartnerCreatebyVAT, self).setUp()
        self.partner_model = self.env['res.partner']
        self.sample_1 = {
            'valid': True,
            'name': u'SA ODOO',
            'address': u'Chaussée De Namur 40 1367 Ramillies',
        }

    def test_create_from_vat1(self):
        # Create an partner from VAT number field
        self.partner1_id = self.partner_model.create({'name': '1',
                                                      'vat': 'be0477472701',
                                                      'is_company': True})

        with mock.patch(mock_vies) as mock_func:
            mock_func.return_value = type('obj', (object,), self.sample_1)
            # Push the button to fetch partner's data
            self.partner1_id.get_vies_data_from_vat()

        # Check if the datas fetch correspond with the datas from VIES.
        self.assertEqual(
            unicode(self.partner1_id.name), self.sample_1['name'])
        self.assertEqual(
            unicode(self.partner1_id.street), self.sample_1['address'])
        self.assertEqual(self.partner1_id.country_id.name, 'Belgium')
        self.assertEqual(self.partner1_id.vat, 'BE0477472701')
        self.assertEqual(self.partner1_id.vat_subjected, True)

    def test_vat_change1(self):
        # Create an partner from VAT number field
        self.partner11_id = self.partner_model.create({'name': '1',
                                                      'is_company': True})

        with self.env.do_in_onchange():
            with mock.patch(mock_vies) as mock_func:
                mock_func.return_value = type('obj', (object,), self.sample_1)
                self.partner11_id.vat = 'be0477472701'
                res = self.partner11_id.vat_change()
            self.partner11_id.update(res['value'])

            # Check if the datas fetch correspond with the datas from VIES.
            self.assertEqual(
                unicode(self.partner11_id.name), self.sample_1['name'])
            self.assertEqual(
                unicode(self.partner11_id.street), self.sample_1['address'])
            self.assertEqual(self.partner11_id.country_id.name, 'Belgium')
            self.assertEqual(self.partner11_id.vat, 'BE0477472701')
            self.assertEqual(self.partner11_id.vat_subjected, True)

    def test_create_from_vat2(self):
        # Create an partner from VAT number field
        self.partner2_id = self.partner_model.create({'name': '1',
                                                      'vat': 'ro4400972',
                                                      'is_company': True})

        # Check VAT number not listed on VIES
        with self.assertRaises(ValidationError):
            self.partner2_id.get_vies_data_from_vat()
