# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestPartnerCreatebyVAT(TransactionCase):

    def setUp(self):
        super(TestPartnerCreatebyVAT, self).setUp()
        self.partner_model = self.env['res.partner']

    def test_create_from_vat1(self):
        # Create an partner from VAT number field
        self.partner1_id = self.partner_model.create({'name': '1',
                                                      'vat': 'be0477472701',
                                                      'is_company': True})

        # Push the button to fetch partner's data
        self.partner1_id.get_vies_data_from_vat()

        # Check if the datas fetch correspond with the datas from VIES.
        self.assertEqual(self.partner1_id.name, 'SA ODOO')
        self.assertEqual(
            unicode(self.partner1_id.street),
            u'Chaussée De Namur 40 1367 Ramillies'
        )
        self.assertEqual(self.partner1_id.country_id.name, 'Belgium')
        self.assertEqual(self.partner1_id.vat, 'BE0477472701')
        self.assertEqual(self.partner1_id.vat_subjected, True)

    def test_vat_change1(self):
        # Create an partner from VAT number field
        self.partner11_id = self.partner_model.create({'name': '1',
                                                      'is_company': True})

        with self.env.do_in_onchange():
            res = self.partner11_id.vat_change('be0477472701')
            self.partner11_id.update(res['value'])

            # Check if the datas fetch correspond with the datas from VIES.
            self.assertEqual(self.partner11_id.name, 'SA ODOO')
            self.assertEqual(
                unicode(self.partner11_id.street),
                u'Chaussée De Namur 40 1367 Ramillies'
            )
            self.assertEqual(self.partner11_id.country_id.name, 'Belgium')
            self.assertEqual(self.partner11_id.vat, 'BE0477472701')
            self.assertEqual(self.partner11_id.vat_subjected, True)

    def test_create_from_vat2(self):
        # Create an partner from VAT number field
        self.partner2_id = self.partner_model.create({'name': '1',
                                                      'vat': 'ro16507426',
                                                      'is_company': True})

        # Check VAT number not listed on VIES
        with self.assertRaises(ValidationError):
            self.partner2_id.get_vies_data_from_vat()
