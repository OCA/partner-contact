# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp import fields
from dateutil.relativedelta import relativedelta
from datetime import datetime


class TestPartnerFinancialRisk(TransactionCase):

    def setUp(self):
        super(TestPartnerFinancialRisk, self).setUp()
        self.env.user.groups_id |= self.env.ref('base.group_sale_manager')
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        self.journal = self.env['account.journal'].create({
            'type': 'sale',
            'name': 'Test Sales',
            'code': 'TSALE',
        })
        self.prod_account = self.env.ref('account.a_sale')
        self.inv_account = self.env.ref('account.a_recv')
        date_inv = datetime.now() - relativedelta(days=7)
        date_due = datetime.now() - relativedelta(days=3)
        self.invoice = self.env['account.invoice'].create({
            'journal_id': self.journal.id,
            'company_id': self.env.user.company_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'date_invoice': date_inv.strftime("%Y-%m-%d"),
            'date_due': date_due.strftime("%Y-%m-%d"),
            'partner_id': self.partner.id,
            'account_id': self.inv_account.id,
            'invoice_line': [(0, 0, {
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
        self.partner.risk_invoice_unpaid_include = True
        self.assertAlmostEqual(self.partner.risk_invoice_unpaid, 500.0)
        self.assertAlmostEqual(self.partner.risk_total, 500.0)
        self.partner.credit_limit = 100.0
        self.assertTrue(self.partner.risk_exception)
        self.partner.credit_limit = 1000.0
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_invoice_unpaid_limit = 499.0
        self.assertTrue(self.partner.risk_exception)
        invoice2 = self.invoice.copy()
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg, "Financial risk exceeded.\n")
        self.partner.risk_invoice_unpaid_limit = 0.0
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_invoice_open_limit = 300.0
        invoice2.date_due = fields.Date.today()
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         "This invoice exceeds the open invoices risk.\n")
        self.partner.risk_invoice_open_limit = 0.0
        self.partner.risk_invoice_draft_include = False
        self.partner.risk_invoice_open_include = True
        self.partner.credit_limit = 900.0
        wiz_dic = invoice2.invoice_open()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         "This invoice exceeds the financial risk.\n")
        self.assertAlmostEqual(self.partner.risk_invoice_open, 0.0)
        wiz.button_continue()
        self.assertAlmostEqual(self.partner.risk_invoice_open, 500.0)
        self.assertTrue(self.partner.risk_allow_edit)
        self.partner.process_unpaid_invoices()
        self.assertEqual(self.env['ir.config_parameter'].get_param(
            'partner_financial_risk.last_check'),
            fields.Date.today())
