# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields
from openerp.tests.common import TransactionCase


class TestPartnerFinancialRisk(TransactionCase):
    def setUp(self):
        super(TestPartnerFinancialRisk, self).setUp()
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

    def test_sale_order(self):
        self.sale_order.action_confirm()
        self.assertAlmostEqual(self.partner.risk_sale_order, 100.0)
        self.assertFalse(self.partner.risk_exception)
        self.partner.risk_sale_order_limit = 99
        self.assertTrue(self.partner.risk_exception)
        self.partner.risk_sale_order_limit = 0.0

        invoice_so_id = self.sale_order.action_invoice_create()
        self.assertAlmostEqual(self.partner.risk_invoice_draft, 100.0)
        invoice_so = self.env['account.invoice'].browse(invoice_so_id)
        invoice_so.date_due = fields.Date.today()
        invoice_so.signal_workflow('invoice_open')
        self.assertAlmostEqual(self.partner.risk_invoice_open, 100.0)

        self.partner.risk_invoice_open_include = True
        self.assertAlmostEqual(self.partner.risk_total, 100.0)
        self.assertTrue(self.partner.risk_exception)
        self.partner.credit_limit = 100.0
        self.assertFalse(self.partner.risk_exception)
