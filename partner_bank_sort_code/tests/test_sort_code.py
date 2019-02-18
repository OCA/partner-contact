# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from psycopg2 import IntegrityError


class TestSortCode(common.TransactionCase):

    def setUp(self):
        super(TestSortCode, self).setUp()
        # Create two different active bank with different sort codes

        self.bank_obj = self.env['res.bank']

        vals = {
            'name': 'BANK 1',
            'sort_code': '95-01-32',
        }
        self.bank_1 = self.bank_obj.create(vals)

        vals = {
            'name': 'BANK 2',
            'sort_code': '95-01-33',
        }
        self.bank_2 = self.bank_obj.create(vals)

    def test_sort_code_duplicate(self):
        # Create a duplicate
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-32',
        }
        with self.assertRaises(IntegrityError):
            self.bank_obj.create(vals)

    def test_sort_code(self):
        # Create a new bank with new sort code
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-34',
        }
        self.bank_obj.create(vals)

    def test_sort_code_inactive(self):
        # Set several banks with same sort code to inactive and then create
        # a bank with that sort code
        self.bank_1.write({'active': False})
        vals = {
            'name': 'BANK 3',
            'sort_code': '95-01-32',
        }
        self.bank_3 = self.bank_obj.create(vals)
        self.bank_3.active = False

        vals = {
            'name': 'BANK 4',
            'sort_code': '95-01-32',
        }
        self.bank_obj.create(vals)
