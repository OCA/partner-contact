# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestPartnerSaleRisk(AccountingTestCase):
    def setUp(self):
        super(TestPartnerSaleRisk, self).setUp()
        self.env.user.groups_id |= self.env.ref('sales_team.group_sale_manager')
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        self.product = self.env.ref('product.product_product_2')
        self.product.invoice_policy = 'order'
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'pricelist_id': self.env.ref('product.list0').id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'product_uom': self.product.uom_id.id,
                'price_unit': 100.0})],
        })
        self.env.user.lang = 'en_US'

    def test_sale_order(self):
        self.sale_order.action_confirm()
        self.assertAlmostEqual(self.partner.risk_sale_order, 100.0)
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_sale_order_limit = 99.0
        self.assertTrue(self.partner.risk_exception)
        sale_order2 = self.sale_order.copy()
        wiz_dic = sale_order2.action_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg, "Financial risk exceeded.\n")
        self.partner.risk_sale_order_limit = 150.0
        wiz_dic = sale_order2.action_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         "This sale order exceeds the sales orders risk.\n")
        self.partner.risk_sale_order_limit = 0.0
        self.partner.risk_sale_order_include = True
        self.partner.credit_limit = 100.0
        wiz_dic = sale_order2.action_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(wiz.exception_msg,
                         "This sale order exceeds the financial risk.\n")
        self.assertTrue(self.partner.risk_allow_edit)
        wiz.button_continue()
        self.assertAlmostEqual(self.partner.risk_sale_order, 200.0)

    def test_invoice_amount(self):
        self.sale_order.action_confirm()
        self.assertAlmostEqual(self.sale_order.invoice_pending_amount, 100.0)
        self.assertAlmostEqual(self.sale_order.invoice_amount, 0.0)
        wizard = self.env['sale.advance.payment.inv'].with_context({
            'active_id': self.sale_order.id,
            'active_ids': [self.sale_order.id],
            'active_model': 'sale.order',
        }).create({
            'advance_payment_method': 'percentage',
            'amount': 80,
        })
        wizard.create_invoices()
        self.assertAlmostEqual(self.sale_order.invoice_pending_amount, 20.0)
        self.assertAlmostEqual(self.sale_order.invoice_amount, 80.0)
