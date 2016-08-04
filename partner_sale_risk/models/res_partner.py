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
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount')
    def _compute_risk_sale_order(self):
        for partner in self:
            partner.risk_sale_order = sum(
                partner.sale_order_ids.mapped('invoice_pending_amount'))

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_sale_order', 'risk_sale_order_limit',
                    'risk_sale_order_include'))
        return res
