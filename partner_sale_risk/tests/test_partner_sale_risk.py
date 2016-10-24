# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import SavepointCase


class TestPartnerSaleRisk(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerSaleRisk, cls).setUpClass()
        cls.env.user.groups_id |= cls.env.ref('base.group_sale_manager')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        cls.product = cls.env.ref('product.product_product_2')
        cls.product.invoice_policy = 'order'
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'pricelist_id': cls.env.ref('product.list0').id,
            'order_line': [(0, 0, {
                'name': cls.product.name,
                'product_id': cls.product.id,
                'product_uom_qty': 1,
                'product_uom': cls.product.uom_id.id,
                'price_unit': 100.0})],
        })
        cls.env.user.lang = 'en_US'

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
        self.sale_order.action_invoice_create()
        self.assertAlmostEqual(self.sale_order.invoice_pending_amount, 0.0)
        self.assertAlmostEqual(self.sale_order.invoice_amount, 100.0)
