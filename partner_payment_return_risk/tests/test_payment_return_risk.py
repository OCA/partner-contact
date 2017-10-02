# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestPartnerPaymentReturnRisk(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerPaymentReturnRisk, cls).setUpClass()
        cls.journal = cls.env['account.journal'].create({
            'name': 'Test Sales Journal',
            'code': 'tVEN',
            'type': 'sale',
            'update_posted': True,
        })
        cls.bank_journal = cls.env['account.journal'].create({
            'name': 'Test Bank Journal',
            'code': 'BANK',
            'type': 'bank',
            'update_posted': True,
        })
        cls.account_type = cls.env['account.account.type'].create({
            'name': 'Test',
            'type': 'receivable',
        })
        cls.account = cls.env['account.account'].create({
            'name': 'Test account',
            'code': 'TEST',
            'user_type_id': cls.account_type.id,
            'reconcile': True,
        })
        cls.account_income = cls.env['account.account'].create({
            'name': 'Test income account',
            'code': 'INCOME',
            'user_type_id': cls.env['account.account.type'].create(
                {'name': 'Test income'}).id,
        })
        cls.partner = cls.env['res.partner'].create({'name': 'Test'})
        cls.invoice = cls.env['account.invoice'].create({
            'journal_id': cls.journal.id,
            'account_id': cls.account.id,
            'company_id': cls.env.user.company_id.id,
            'currency_id': cls.env.user.company_id.currency_id.id,
            'partner_id': cls.partner.id,
            'invoice_line_ids': [(0, 0, {
                'account_id': cls.account_income.id,
                'name': 'Test line',
                'price_unit': 50,
                'quantity': 10,
            })]
        })
        cls.reason = cls.env['payment.return.reason'].create({
            'code': 'RTEST',
            'name': 'Reason Test'
        })
        cls.invoice.signal_workflow('invoice_open')
        cls.receivable_line = cls.invoice.move_id.line_ids.filtered(
            lambda x: x.account_id.internal_type == 'receivable')
        # Invert the move to simulate the payment
        cls.payment_move = cls.invoice.move_id.copy({
            'journal_id': cls.bank_journal.id
        })
        for move_line in cls.payment_move.line_ids:
            move_line.with_context(check_move_validity=False).write({
                'debit': move_line.credit, 'credit': move_line.debit})
        cls.payment_line = cls.payment_move.line_ids.filtered(
            lambda x: x.account_id.internal_type == 'receivable')
        # Reconcile both
        (cls.receivable_line | cls.payment_line).reconcile()
        # Create payment return
        cls.payment_return = cls.env['payment.return'].create(
            {'journal_id': cls.bank_journal.id,
             'line_ids': [
                 (0, 0, {'partner_id': cls.partner.id,
                         'move_line_ids': [(6, 0, cls.payment_line.ids)],
                         'amount': cls.payment_line.credit})]})

    def test_payment_return_risk(self):
        self.assertAlmostEqual(self.partner.risk_payment_return, 0.0)
        self.payment_return.action_confirm()
        self.assertAlmostEqual(self.partner.risk_payment_return, 500.0)
        self.payment_return.action_cancel()
        self.assertAlmostEqual(self.partner.risk_payment_return, 0.0)
