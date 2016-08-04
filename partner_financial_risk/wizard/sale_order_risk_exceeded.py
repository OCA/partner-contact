# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SaleOrderRiskExceeded(models.TransientModel):
    _name = 'sale.order.risk.exceeded'

    partner_id = fields.Many2one(
        comodel_name='res.partner', readonly=True, string='Customer')
    exception_msg = fields.Text(readonly=True)

    @api.multi
    def button_continue(self):
        self.ensure_one()
        so = self.env['sale.order'].browse(self.env.context['active_id'])
        return so.with_context(bypass_risk=True).action_confirm()
