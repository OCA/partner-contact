# -*- coding: utf-8 -*-
# © 2015 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    profitseg_segment_id = fields.Many2one(
        'res.partner.profitseg.segment',
        compute='get_profit_segment',
        string='Profit segment')

    @api.one
    def get_profit_segment(self):
        total_turnover = 0.0
        total_cost = 0.0
        for inv_line in self.env['account.invoice.line'].search(
            [('partner_id', '=', self.id),
             ('invoice_id.date_invoice', '>=', time.strftime('%Y-01-01')),
             ('product_id', '!=', False),
             ]):
            total_turnover += inv_line.price_subtotal
            standard_price = inv_line.product_id.standard_price
            total_cost += standard_price * inv_line.quantity
        profit = total_turnover - total_cost
        segments = self.env['res.partner.profitseg.segment'].search(
            [('lower_limit', '<=', profit),
             ('upper_limit', '>', profit)
             ])
        self.profitseg_segment_id = False
        if segments:
            self.profitseg_segment_id = segments[0].id
