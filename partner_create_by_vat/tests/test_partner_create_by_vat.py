# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

from openerp.tests.common import TransactionCase


class TestPartnerCreatebyVAT(TransactionCase):
    def setUp(self):
        super(TestPartnerCreatebyVAT, self).setUp()
        self.partner_model = self.env['res.partner']

    def test_create_from_name(self):
        # Create an partner with VAT number in name field
        self.partner1_id = self.partner_model.create({'name': 'BE0477472701'})

        # Push the button to fetch partner's data
        self.partner1_id.button_get_partner_data()

        # Check if the datas fetch correspond with the datas from VIES.
        self.assertTrue(self.partner1_id.name == 'SA ODOO')
        self.assertTrue(
            unicode(self.partner1_id.street) == u'Chaussée De Namur 40 1367 '
                                                 'Ramillies')
        self.assertTrue(self.partner1_id.country_id.name == 'Belgium')
        self.assertTrue(self.partner1_id.vat == 'BE0477472701')
        self.assertTrue(self.partner1_id.vat_subjected == True)

    def test_create_from_vat(self):
        # Create an partner with VAT number in name field
        self.partner2_id = self.partner_model.create({'name': ' ',
                                                      'vat': 'be0477472701'})

        # Push the button to fetch partner's data
        self.partner2_id.button_get_partner_data()

        # Check if the datas fetch correspond with the datas from VIES.
        self.assertTrue(self.partner2_id.name == 'SA ODOO')
        self.assertTrue(
            unicode(self.partner2_id.street) == u'Chaussée De Namur 40 1367 '
                                                 'Ramillies')
        self.assertTrue(self.partner2_id.country_id.name == 'Belgium')
        self.assertTrue(self.partner2_id.vat == 'BE0477472701')
        self.assertTrue(self.partner2_id.vat_subjected == True)
