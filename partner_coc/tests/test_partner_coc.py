# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPartnerCoC(TransactionCase):
    def setUp(self):
        super(TestPartnerCoC, self).setUp()
        self.main_partner = self.env.ref('base.main_partner')
        self.partner_id_category = self.env.ref('partner_coc.id_category_coc')

    def test_01_id_number_new(self):
        # Good CoC
        vals = {
            'name': '56048785',
            'category_id': self.partner_id_category.id,
        }
        self.main_partner.write({'id_numbers': [(0, 0, vals)]})
        id_number = self.main_partner.id_numbers[0]

        self.assertEqual(id_number.name, '56048785')

    def test_02_id_number_duplicate(self):
        # Duplicate CoC
        vals = {
            'name': '56048785',
            'category_id': self.partner_id_category.id,
        }

        self.main_partner.write({'id_numbers': [(0, 0, vals)]})
        id_number_name = self.main_partner.id_numbers[0].name
        self.assertEqual(id_number_name, '56048785')

        new_partner = self.env['res.partner'].create({'name': 'Test Partner'})

        new_partner.write({'id_numbers': [(0, 0, vals)]})
        id_number_name = new_partner.id_numbers[0].name
        self.assertEqual(id_number_name, '56048785')

    def test_03_coc_registration_number_create(self):
        new_partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'coc_registration_number': '56048785',
        })

        self.assertEqual(new_partner.coc_registration_number, '56048785')

        id_numbers = new_partner.id_numbers
        self.assertTrue(id_numbers)
        self.assertEqual(len(id_numbers), 1)
        self.assertEqual(id_numbers.name, '56048785')

    def test_04_coc_registration_number_write(self):
        self.main_partner.write({
            'coc_registration_number': '56048785'
        })
        coc = self.main_partner.coc_registration_number
        self.assertEqual(coc, '56048785')

        id_numbers = self.main_partner.id_numbers
        self.assertTrue(id_numbers)
        self.assertEqual(len(id_numbers), 1)
        self.assertEqual(id_numbers.name, '56048785')
