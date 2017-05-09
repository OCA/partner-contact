# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests import common


class TestPartnerPaymentReturnRisk(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPartnerPaymentReturnRisk, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
            'risk_payment_return_include': True,
            'risk_payment_return_limit': 50.0,
        })
        cls.user_type = cls.env.ref('account.data_account_type_revenue')
        cls.invoice = cls.env['account.invoice'].create({
            'partner_id': cls.partner.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Product Test',
                'quantity': 1.0,
                'uom_id': cls.env.ref('product.product_uom_unit').id,
                'price_unit': 100.0,
                'account_id': cls.env['account.account'].search([
                    ('user_type_id', '=', cls.user_type.id)], limit=1).id,
            })]
        })

    def test_payment_return_risk(self):
        self.invoice.signal_workflow('invoice_open')
        # Partner risk is zero because invoice is not returned
        self.assertAlmostEqual(self.partner.risk_payment_return, 0.0)
        # We simulate that the invoice is returned
        self.invoice.returned_payment = True
        # Partner risk has increased
        self.assertAlmostEqual(self.partner.risk_payment_return, 100.0)
