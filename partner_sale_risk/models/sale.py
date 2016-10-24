# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_amount = fields.Monetary(
        compute='_compute_invoice_amount', store=True)
    invoice_pending_amount = fields.Monetary(
        compute='_compute_invoice_amount', store=True)

    @api.multi
    @api.depends('state', 'order_line.invoice_lines.invoice_id.amount_total')
    def _compute_invoice_amount(self):
        AccountInvoice = self.env['account.invoice']
        for order in self.filtered(lambda x: x.state == 'sale'):
            invoice_ids = order.order_line.mapped(
                'invoice_lines.invoice_id').ids
            if not invoice_ids:
                order.invoice_pending_amount = order.amount_total
                continue
            amount = AccountInvoice.read_group(
                [('id', 'in', invoice_ids),
                 ('type', 'in', ['out_invoice', 'out_refund'])],
                ['amount_total'],
                []
            )[0]['amount_total']
            order.invoice_amount = amount
            if order.amount_total > amount:
                order.invoice_pending_amount = order.amount_total - amount

    @api.multi
    def action_confirm(self):
        if not self.env.context.get('bypass_risk', False):
            partner = self.partner_id.commercial_partner_id
            exception_msg = ""
            if partner.risk_exception:
                exception_msg = _("Financial risk exceeded.\n")
            elif partner.risk_sale_order_limit and (
                    (partner.risk_sale_order + self.amount_total) >
                    partner.risk_sale_order_limit):
                exception_msg = _(
                    "This sale order exceeds the sales orders risk.\n")
            elif partner.risk_sale_order_include and (
                    (partner.risk_total + self.amount_total) >
                    partner.credit_limit):
                exception_msg = _(
                    "This sale order exceeds the financial risk.\n")
            if exception_msg:
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': partner.id,
                    'origin_reference': '%s,%s' % (self._model, self.id),
                    'continue_method': 'action_confirm',
                }).action_show()
        return super(SaleOrder, self).action_confirm()
