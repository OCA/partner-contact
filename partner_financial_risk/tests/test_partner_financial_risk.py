# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import SavepointCase
from openerp import fields


class TestPartnerFinancialRisk(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerFinancialRisk, cls).setUpClass()
        cls.env.user.groups_id |= cls.env.ref('base.group_sale_manager')
        type_revenue = cls.env.ref('account.data_account_type_revenue')
        type_receivable = cls.env.ref('account.data_account_type_receivable')
        tax_group_taxes = cls.env.ref('account.tax_group_taxes')
        cls.account_sale = cls.env['account.account'].create({
            'name': 'Sale',
            'code': 'XX_700',
            'user_type_id': type_revenue.id,
            'reconcile': True,
        })
        cls.account_customer = cls.env['account.account'].create({
            'name': 'Customer',
            'code': 'XX_430',
            'user_type_id': type_receivable.id,
            'reconcile': True,
        })
        cls.other_account_customer = cls.env['account.account'].create({
            'name': 'Other Account Customer',
            'code': 'XX_431',
            'user_type_id': type_receivable.id,
            'reconcile': True,
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
            'property_account_receivable_id': cls.account_customer.id,
        })
        cls.invoice_address = cls.env['res.partner'].create({
            'name': 'Partner test invoice',
            'parent_id': cls.partner.id,
            'type': 'invoice',
        })
        cls.journal_sale = cls.env['account.journal'].create({
            'name': 'Test journal for sale',
            'type': 'sale',
            'code': 'TSALE',
            'default_debit_account_id': cls.account_sale.id,
            'default_credit_account_id': cls.account_sale.id,
        })
        cls.tax = cls.env['account.tax'].create({
            'name': 'Tax for sale 10%',
            'type_tax_use': 'sale',
            'tax_group_id': tax_group_taxes.id,
            'amount_type': 'percent',
            'amount': 10.0,
        })
        cls.invoice = cls.env['account.invoice'].create({
            'partner_id': cls.partner.id,
            'account_id': cls.account_customer.id,
            'type': 'out_invoice',
            'journal_id': cls.journal_sale.id,
            'payment_term_id': False,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test product',
                'account_id': cls.account_sale.id,
                'price_unit': 50,
                'quantity': 10,
                'invoice_line_tax_ids': [(6, 0, [cls.tax.id])],
            })],
        })

    def test_invoices(self):
        self.partner.risk_invoice_draft_include = True
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 550.0)
        self.assertAlmostEqual(self.partner.risk_total, 550.0)
        self.invoice.signal_workflow('invoice_open')
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 0.0)
        line = self.invoice.move_id.line_ids.filtered(lambda x: x.debit != 0.0)
        line.date_maturity = '2017-01-01'
        self.partner.risk_invoice_unpaid_include = True
        self.assertAlmostEqual(self.partner.risk_total, 550.0)
        self.partner.credit_limit = 100.0
        self.assertTrue(self.partner.risk_exception)
        self.partner.credit_limit = 1100.0
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_invoice_unpaid_limit = 499.0
        self.assertTrue(self.partner.risk_exception)
        invoice2 = self.invoice.copy({'partner_id': self.invoice_address.id})
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 550.0)
        self.assertAlmostEqual(self.partner.risk_invoice_unpaid, 550.0)
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
        self.assertAlmostEqual(self.partner.risk_invoice_open, 550.0)
        self.assertTrue(self.partner.risk_allow_edit)
        self.partner.process_unpaid_invoices()
        self.assertEqual(self.env['ir.config_parameter'].get_param(
            'partner_financial_risk.last_check'),
            fields.Date.today())

    def test_other_account_amount(self):
        self.move = self.env['account.move'].create({
            'journal_id': self.journal_sale.id,
            'date': fields.Date.today(),
            'line_ids': [
                (0, 0, {
                    'name': 'Debit line',
                    'partner_id': self.partner.id,
                    'account_id': self.other_account_customer.id,
                    'debit': 100,
                }),
                (0, 0, {
                    'name': 'Credit line',
                    'partner_id': self.partner.id,
                    'account_id': self.account_sale.id,
                    'credit': 100,
                }),
            ],
        })
        self.assertAlmostEqual(self.partner.risk_account_amount, 100.0)
        line = self.move.line_ids.filtered(lambda x: x.debit != 0.0)
        line.date_maturity = '2017-01-01'
        self.assertAlmostEqual(self.partner.risk_account_amount, 0.0)
        self.assertAlmostEqual(self.partner.risk_account_amount_unpaid, 100.0)

    def test_recompute_newid(self):
        """Computing risk shouldn't fail if record is a NewId."""
        new = self.env["res.partner"].new({"customer": True})
        new._compute_risk_invoice()
