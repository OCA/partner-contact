# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestPartnerFinancialRisk(TransactionCase):
    def setUp(self):
        super(TestPartnerFinancialRisk, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'test',
        })

    def test_partner_financial_risk(self):
        self.assertEqual(self.partner.name, 'test')
