# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import exceptions
from openerp.tests.common import SavepointCase


class TestPartnerStocklRisk(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPartnerStocklRisk, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner test',
            'customer': True,
        })
        cls.product = cls.env.ref('product.product_product_36')
        cls.quant = cls.env['stock.quant'].create({
            'qty': 100,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'product_id': cls.product.id,
        })
        cls.picking = cls.env['stock.picking'].create({
            'picking_type_id': cls.env.ref('stock.picking_type_out').id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'location_dest_id':
                cls.env.ref('stock.stock_location_customers').id,
            'partner_id': cls.partner.id,
        })
        cls.move = cls.env['stock.move'].create({
            'name': '/',
            'picking_id': cls.picking.id,
            'product_uom_qty': 10,
            'product_uom': cls.product.uom_id.id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'location_dest_id':
                cls.env.ref('stock.stock_location_customers').id,
            'product_id': cls.product.id,
        })
        cls.env.user.lang = 'en_US'

    def test_stock_move_ok(self):
        self.move.action_done()

    def test_stock_move_error(self):
        self.partner.risk_exception = True
        self.move.partner_id = self.partner
        with self.assertRaises(exceptions.UserError):
            self.move.action_done()

    def test_stock_picking_ok(self):
        self.picking.action_assign()
        self.picking.force_assign()
        self.picking.action_confirm()

    def test_stock_picking_error(self):
        self.partner.risk_exception = True
        res = self.picking.action_assign()
        self.assertEqual(res['name'], 'Partner risk exceeded')
        res = self.picking.force_assign()
        self.assertEqual(res['name'], 'Partner risk exceeded')
        res = self.picking.action_confirm()
        self.assertEqual(res['name'], 'Partner risk exceeded')

    def test_do_new_transfer_ok(self):
        self.picking.action_assign()
        self.picking.pack_operation_product_ids[:1].qty_done = 5
        self.picking.do_new_transfer()

    def test_do_new_transfer_error(self):
        self.picking.action_assign()
        self.picking.pack_operation_product_ids[:1].qty_done = 5
        self.partner.risk_exception = True
        res = self.picking.do_new_transfer()
        self.assertEqual(res['name'], 'Partner risk exceeded')
