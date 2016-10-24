# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_sale_order_include = fields.Boolean(
        string='Include Sales Orders', help='Full risk computation')
    risk_sale_order_limit = fields.Monetary(
        string='Limit Sales Orders', help='Set 0 if it is not locked')
    risk_sale_order = fields.Monetary(
        compute='_compute_risk_sale_order', store=True,
        string='Total Sales Orders Not Invoiced',
        help='Total not invoiced of sales orders in Sale Order state')

    @api.multi
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount',
                 'child_ids.sale_order_ids',
                 'child_ids.sale_order_ids.invoice_pending_amount')
    def _compute_risk_sale_order(self):
        customers = self.filtered('customer')
        partners = customers | customers.mapped('child_ids')
        orders_group = self.env['sale.order'].read_group(
            [('state', '=', 'sale'), ('partner_id', 'in', partners.ids)],
            ['partner_id', 'invoice_pending_amount'],
            ['partner_id'])
        for partner in customers:
            partner_ids = (partner | partner.child_ids).ids
            partner.risk_sale_order = sum(
                [x['invoice_pending_amount']
                 for x in orders_group if x['partner_id'][0] in partner_ids])

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_sale_order', 'risk_sale_order_limit',
                    'risk_sale_order_include'))
        return res
