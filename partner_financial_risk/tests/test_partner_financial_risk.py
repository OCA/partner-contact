# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestPartnerFinancialRisk(TransactionCase):
    def setUp(self):
        super(TestPartnerFinancialRisk, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        self.journal = self.env['account.journal'].create({
            'type': 'sale',
            'name': 'Test Sales',
            'code': 'TSALE',
        })
        self.prod_account = self.env.ref('account.demo_coffee_machine_account')
        self.inv_account = self.env.ref('account.demo_sale_of_land_account')
        self.invoice = self.env['account.invoice'].create({
            'journal_id': self.journal.id,
            'company_id': self.env.user.company_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'partner_id': self.partner.id,
            'invoice_line_ids': [(0, 0, {
                'account_id': self.prod_account.id,
                'name': 'Test line',
                'price_unit': 50,
                'quantity': 10,
            })]
        })

    def test_invoices(self):
        self.partner.risk_invoice_draft_include = True
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 500.0)
        self.assertAlmostEqual(self.partner.risk_total, 500.0)
        self.invoice.signal_workflow('invoice_open')
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 0.0)
        self.assertFalse(self.invoice.date_due)
        self.partner.risk_invoice_unpaid_include = True
        self.assertAlmostEqual(self.partner.risk_total, 500.0)
        self.partner.credit_limit = 100.0
        self.assertTrue(self.partner.risk_exception)
        self.partner.credit_limit = 1000.0
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_invoice_unpaid_limit = 499.0
        self.assertTrue(self.partner.risk_exception)
