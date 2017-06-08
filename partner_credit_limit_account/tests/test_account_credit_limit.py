# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 UAB Versada
#    (<http://www.versada.lt>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestCreditLimit(common.TransactionCase):

    def setUp(self):

        super(TestCreditLimit, self).setUp()

        self.partner_model = self.env['res.partner']
        self.move_model = self.env['account.move']
        self.sales_journal_id = self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1)

        self.credit_account_id = self.env['account.account'].search(
            [('type', '=', 'other')], limit=1).id

        self.partner_company = self.partner_model.create({
            'name': 'Test Company',
            'is_company': True,
            'credit_limit': 100,
        })

        self.partner_company_contact = self.partner_model.create({
            'name': 'Test Contact',
            'is_company': False,
            'parent_id': self.partner_company.id,
        })

        self.line_id_1 = [(0, 0, {
            'name': 'Debit Line',
            'partner_id': self.partner_company.id,
            'account_id': self.partner_company.property_account_receivable.id,
            'debit': 99}),
            (0, 0, {
                'name': 'Debit Line',
                'partner_id': self.partner_company.id,
                'account_id': self.credit_account_id,
                'credit': 99}),
        ]

        self.line_id_2 = [(0, 0, {
            'name': 'Debit Line',
            'partner_id': self.partner_company.id,
            'account_id': self.partner_company.property_account_receivable.id,
            'debit': 101}),
            (0, 0, {
                'name': 'Debit Line',
                'partner_id': self.partner_company.id,
                'account_id': self.credit_account_id,
                'credit': 101}),
        ]

    def test_credit_limit_validates(self):

        self.assertTrue(
            self.move_model.create({
                'journal_id': self.sales_journal_id.id,
                'line_id': self.line_id_1,
                'state': 'draft'
            }).validate()
        )

    def test_credit_limit_not_validates(self):

        self.move_model.create({
            'journal_id': self.sales_journal_id.id,
            'line_id': self.line_id_1,
            'state': 'draft'
        }).validate()

        with self.assertRaises(ValidationError):
            self.move_model.create({
                'journal_id': self.sales_journal_id.id,
                'line_id': self.line_id_2,
                'state': 'draft'
            }).validate()
