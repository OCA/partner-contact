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

        self.partner = self.partner_model.create({
            'name': 'Test Partner',
            'is_company': False,
            'credit_limit': 100,
        })

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

    def test_credit_limit_not_reached(self):

        self.assertIsNone(
            self.partner.credit_limit_reached(
                credit_increase=99)
        )

        self.assertIsNone(
            self.partner_company.credit_limit_reached(
                credit_increase=99)
        )

        self.assertIsNone(
            self.partner_company_contact.credit_limit_reached(
                credit_increase=99)
        )

    def test_credit_limit_raises(self):

        with self.assertRaises(ValidationError):
            self.partner.credit_limit_reached(
                credit_increase=101)

        with self.assertRaises(ValidationError):
            self.partner_company.credit_limit_reached(
                credit_increase=101)

        with self.assertRaises(ValidationError):
            self.partner_company_contact.credit_limit_reached(
                credit_increase=101)

    def test_credit_limit_not_raises(self):

        self.assertTrue(
            self.partner.credit_limit_reached(
                credit_increase=101, raise_error=False)
        )

        self.assertTrue(
            self.partner_company.credit_limit_reached(
                credit_increase=101, raise_error=False)
        )

        self.assertTrue(
            self.partner_company_contact.credit_limit_reached(
                credit_increase=101, raise_error=False)
        )
