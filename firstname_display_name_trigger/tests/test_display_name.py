# -*- coding: utf-8 -*-
import unittest2

import openerp.tests.common as common


class test_display_name(common.TransactionCase):

    def setUp(self):
        super(test_display_name, self).setUp()
        self.res_partner = self.registry('res.partner')

    def test_00_create_res_partner(self):
        """ Test if the display name has been correctly set """
        cr, uid = self.cr, self.uid
        partner_id = self.res_partner.create(cr, uid, {
            'lastname': 'Lastname',
            'firstname': 'Firstname',
            'is_company': True,
        })
        partner_records = self.res_partner.browse(cr, uid, [partner_id])
        p1 = partner_records[0]
        self.assertEqual(
            p1.display_name,
            'Lastname Firstname',
            'Partner display_name incorrect'
        )

    def test_01_res_partner_write_lastname(self):
        """ Test if the display name has been correctly set """
        cr, uid = self.cr, self.uid
        partner_id = self.res_partner.create(cr, uid, {
            'lastname': 'Lastname',
            'firstname': 'Firstname',
            'is_company': True
        })
        partner_records = self.res_partner.browse(cr, uid, [partner_id])
        p1 = partner_records[0]
        self.res_partner.write(cr, uid, partner_id, {'lastname': 'Last'})
        self.assertEqual(
            p1.display_name,
            'Last Firstname',
            'Partner display_name incorrect'
        )


if __name__ == '__main__':
    unittest2.main()
