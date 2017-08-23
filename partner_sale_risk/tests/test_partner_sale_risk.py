# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestPartnerSaleRisk(TransactionCase):

    def setUp(self):
        super(TestPartnerSaleRisk, self).setUp()
        self.env.user.groups_id |= self.env.ref('base.group_sale_manager')
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
        self.wizard = self.env[
            "sale.advance.payment.inv"]

    def test_sale_order_1(self):
        """
        Scenario:
        * 1 sale order @ 100 EUR
        * Manual invoice policy
        * Invoice all
        * Risk sale order not include
        * No invoice risk

        Expected result:
        * Sale order can be confirm
        * Invoice can be validate
        """
        self.sale_order.action_button_confirm()
        self.assertEqual(
            self.sale_order.state,
            "manual")
        wizard = self.wizard.with_context({
            "active_ids": [self.sale_order.id]}).\
            create({
                "advance_payment_method": "all"})
        wizard.create_invoices()
        self.sale_order.invoice_ids.signal_workflow("invoice_open")

    def test_sale_order_2(self):
        """
        Scenario:
        * 1 sale order @ 100 EUR
        * Manual invoice policy
        * Invoice all
        * Sale Order Limit == 75 EUR
        * Risk sale order not include
        * No invoice risk

        Expected result:
        * Sale order exceeds the sale order risk raised
        """

        self.partner.write({
            "risk_sale_order_limit": 75.0,
            "credit_limit": 150.0,
        })
        wiz_dic = self.sale_order.action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(
            wiz.exception_msg,
            "This sale order exceeds the sales orders risk.\n")

    def test_sale_order_3(self):
        """
        Scenario:
        * 1 sale order @ 100 EUR
        * Manual invoice policy
        * Invoice all
        * Sale Order Limit == 100 EUR
        * Credit Limit == 75 EUR
        * Risk sale order include
        * No invoice risk

        Expected result:
        * Sale order exceeds the financial risk raised
        """

        self.partner.write({
            "risk_sale_order_limit": 115.0,
            "credit_limit": 75.0,
            "risk_sale_order_include": True,
        })
        wiz_dic = self.sale_order.action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(
            wiz.exception_msg,
            "This sale order exceeds the financial risk.\n")

    def test_sale_order_4(self):
        """
        Scenario:
        * Sale Order Limit == 100 EUR
        * Credit Limit == 75 EUR
        * Risk sale order include
        * Invoice draft include
        * Sale order #1 @ 100 EUR
        * Manual invoice policy
        * Invoice percentace 0.75
        * Sale order #2 @ 100 EUR
        * Confirm using bypass risk
        * Sale order #3 @ 100 EUR
        * Confirm using bypass risk

        Expected result:
        * Financial risk exceeded raised
        """

        self.partner.write({
            "risk_sale_order_limit": 150.0,
            "credit_limit": 100.0,
            "risk_sale_order_include": True,
            "risk_invoice_draft_include": True,
        })
        self.sale_order.action_button_confirm()
        self.assertEqual(
            self.sale_order.state,
            "manual")
        sale_order2 = self.sale_order.copy()
        sale_order2.order_line[0].write({'price_unit': 10.0})
        sale_order2.with_context(bypass_risk=True).action_button_confirm()
        self.assertTrue(
            self.sale_order.partner_id.risk_exception)
        sale_order3 = self.sale_order.copy()
        sale_order3.order_line[0].write({'price_unit': 10.0})
        wiz_dic = sale_order3.with_context(
            bypass_risk=False).action_button_confirm()
        wiz = self.env[wiz_dic['res_model']].browse(wiz_dic['res_id'])
        self.assertEqual(
            wiz.exception_msg,
            "Financial risk exceeded.\n")
