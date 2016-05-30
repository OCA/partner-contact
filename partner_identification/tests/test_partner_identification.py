# -*- coding: utf-8 -*-
#  ©  2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from psycopg2._psycopg import IntegrityError
import openerp.tests.common as common
from openerp.exceptions import ValidationError


class TestPartnerIdentificationBase(common.TransactionCase):

    def test_base_functionalities(self):
        """Dummy CRUD test
        """
        partner_id_category = self.env['res.partner.id_category'].create({
            'code': 'id_code',
            'name': 'id_name',
        })
        self.assertEqual(partner_id_category.name, 'id_name')
        self.assertEqual(partner_id_category.code, 'id_code')

        partner_1 = self.env.ref('base.res_partner_1')
        self.assertEquals(len(partner_1.id_numbers), 0)
        # create without required category
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            partner_1.write({'id_numbers': [(0, 0, {
                'name': '1234',
            })]})
        # successful creation
        partner_1.write({'id_numbers': [(0, 0, {
            'name': '1234',
            'category_id': partner_id_category.id
        })]})
        self.assertEquals(len(partner_1.id_numbers), 1)
        self.assertEquals(partner_1.id_numbers.name, '1234')
        # delete
        partner_1.write({'id_numbers': [(5, 0, 0)]})
        self.assertEquals(len(partner_1.id_numbers), 0)


class TestPartnerCategoryValidation(common.TransactionCase):

    def test_partner_id_number_validation(self):
        partner_id_category = self.env['res.partner.id_category'].create({
            'code': 'id_code',
            'name': 'id_name',
            'validation_code': """
if id_number.name != '1234':
    failed = True
"""
        })
        partner_1 = self.env.ref('base.res_partner_1')
        with self.assertRaises(ValidationError), self.cr.savepoint():
            partner_1.write({'id_numbers': [(0, 0,  {
                'name': '01234',
                'category_id': partner_id_category.id
            })]})
        partner_1.write({'id_numbers': [(0, 0,  {
            'name': '1234',
            'category_id': partner_id_category.id
        })]})
        self.assertEquals(len(partner_1.id_numbers), 1)
        self.assertEquals(partner_1.id_numbers.name, '1234')

        partner_id_category2 = self.env['res.partner.id_category'].create({
            'code': 'id_code2',
            'name': 'id_name2',
            'validation_code': """
if id_number.name != '1235':
    failed = True
"""})
        # check that the constrains is also checked when we change the
        # associated category
        with self.assertRaises(ValidationError), self.cr.savepoint():
            partner_1.id_numbers.write({
                'category_id': partner_id_category2.id
            })

    def test_bad_calidation_code(self):
        partner_id_category = self.env['res.partner.id_category'].create({
            'code': 'id_code',
            'name': 'id_name',
            'validation_code': """
if id_number.name != '1234' #  missing :
    failed = True
"""
        })
        partner_1 = self.env.ref('base.res_partner_1')
        with self.assertRaises(ValidationError):
            partner_1.write({'id_numbers': [(0, 0,  {
                'name': '1234',
                'category_id': partner_id_category.id
            })]})
