# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        if self.env.context.get('bypass_risk', False):
            return super(AccountInvoice, self).action_invoice_open()
        for invoice in self:
            partner = invoice.partner_id.commercial_partner_id
            exception_msg = ""
            if partner.risk_exception:
                exception_msg = _("Financial risk exceeded.\n")
            elif partner.risk_invoice_open_limit and (
                    (partner.risk_invoice_open + invoice.amount_total) >
                    partner.risk_invoice_open_limit):
                exception_msg = _(
                    "This invoice exceeds the open invoices risk.\n")
            # If risk_invoice_draft_include this invoice included in risk_total
            elif not partner.risk_invoice_draft_include and (
                    partner.risk_invoice_open_include and
                    (partner.risk_total + invoice.amount_total) >
                    partner.credit_limit):
                exception_msg = _(
                    "This invoice exceeds the financial risk.\n")
            if exception_msg:
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': partner.id,
                    'origin_reference':
                        '%s,%s' % ('account.invoice', invoice.id),
                    'continue_method': 'action_invoice_open',
                }).action_show()
        return super(AccountInvoice, self).action_invoice_open()
