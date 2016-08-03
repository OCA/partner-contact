# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, exceptions, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_amount = fields.Monetary(
        compute='_compute_invoice_amount', store=True)
    invoice_pending_amount = fields.Monetary(
        compute='_compute_invoice_amount', store=True)

    @api.multi
    @api.depends('state', 'order_line.invoice_lines.invoice_id.amount_total')
    def _compute_invoice_amount(self):
        for order in self.filtered(lambda x: x.state == 'sale'):
            order.invoice_amount = sum(
                order.invoice_ids.mapped('amount_total'))
            order.invoice_pending_amount = (
                order.amount_total - order.invoice_amount)

    @api.multi
    def action_confirm(self):
        partner = self.partner_id
        if partner.risk_exception:
            raise exceptions.Warning(_(
                "Financial risk exceeded.\n"
                "You can not confirm this sale order"
            ))
        elif partner.risk_sale_order_include and (
                (partner.risk_total + self.amount_total) >
                partner.credit_limit):
            raise exceptions.Warning(_(
                "This sale order exceeds the financial risk.\n"
                "You can not confirm this sale order"
            ))

        return super(SaleOrder, self).action_confirm()
