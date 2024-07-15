# -*- coding: utf-8 -*-
# Copyright 2016 Acsone S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase


class TestGLN(TransactionCase):
    def setUp(self):
        super(TestGLN, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'TestGLN'})
        self.partner2 = self.env['res.partner'].create({'name': 'TestGLN2'})
        pc = self.env.ref('partner_identification_gln.'
                          'partner_identification_gln_number_category')
        self.partner_id_category = pc

        pc_gcp = self.env.ref('partner_identification_gln.'
                              'partner_identification_gcp_number_category')
        self.partner_id_gcp_category = pc_gcp

    def test_gln(self):
        # Good GLN
        vals = {'name': '5450534001717',
                'category_id': self.partner_id_category.id
                }
        self.partner.write({'id_numbers': [(0, 0, vals)]})
        id_number = self.partner.id_numbers[0]

        self.assertEqual(id_number.name, '5450534001717')

        # Duplicate GLN
        vals = {'name': '5450534001717',
                'category_id': self.partner_id_category.id
                }

        with self.assertRaises(ValidationError):
            self.partner2.write({'id_numbers': [(0, 0, vals)]})

        # Bad GLN
        vals = {'name': '5450534001716',
                'category_id': self.partner_id_category.id
                }
        with self.assertRaises(ValidationError):
            self.partner.write({'id_numbers': [(0, 0, vals)]})

    def test_gcp(self):
        # Good GLN
        vals = {'name': '545053',
                'category_id': self.partner_id_gcp_category.id
                }
        self.partner.write({'id_numbers': [(0, 0, vals)]})
        id_number = self.partner.id_numbers[0]

        self.assertEqual(id_number.name, '545053')

        # Duplicate GLN
        vals = {'name': '545053',
                'category_id': self.partner_id_gcp_category.id
                }

        with self.assertRaises(ValidationError):
            self.partner2.write({'id_numbers': [(0, 0, vals)]})

        # Bad GLN
        vals = {'name': '5450534001716',
                'category_id': self.partner_id_gcp_category.id
                }
        with self.assertRaises(ValidationError):
            self.partner.write({'id_numbers': [(0, 0, vals)]})
