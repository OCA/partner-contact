# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    eval_risk_sale_order = fields.Boolean(
        string="Eval Sale Orders", help="Compute in total risk")
    max_risk_sale_order = fields.Monetary(
        string='Max In Sale Orders', help="Set 0 if it not lock")
    risk_sale_order = fields.Monetary(
        compute='_compute_risk_sale_order', store=True,
        string="Sale Order Not Invoiced")

    eval_risk_invoice_draft = fields.Boolean(
        string="Eval Draft Invoices", help="Compute in total risk")
    max_risk_invoice_draft = fields.Monetary(
        string='Max In Draft Invoices', help="Set 0 if it not lock")
    risk_invoice_draft = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string="Not Validated Invoice")

    eval_risk_invoice_open = fields.Boolean(
        string="Eval Open Invoices", help="Compute in total risk")
    max_risk_invoice_open = fields.Monetary(
        string='Max In Open Invoices', help="Set 0 if it not lock")
    risk_invoice_open = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string="Open Invoice")
    eval_risk_invoice_unpaid = fields.Boolean(
        string="Eval Unpaid Invoices", help="Compute in total risk")
    max_risk_invoice_unpaid = fields.Monetary(
        string='Max In Unpaid Invoices', help="Set 0 if it not lock")
    risk_invoice_unpaid = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string="Unpaid Invoice")
    eval_risk_account_amount = fields.Boolean(
        string="Eval Other Account Amount", help="Compute in total risk")
    max_risk_account_amount = fields.Monetary(
        string='Max Other Account Amount', help="Set 0 if it not lock")
    risk_account_amount = fields.Monetary(
        compute='_compute_risk_account_amount',
        string="Other Account Amount")

    risk_total = fields.Monetary(
        string="Total Risk", compute='_compute_risk_exception')
    risk_exception = fields.Boolean(compute='_compute_risk_exception')

    @api.multi
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount')
    def _compute_risk_sale_order(self):
        for partner in self:
            partner.risk_sale_order = sum(
                partner.sale_order_ids.mapped('invoice_pending_amount'))

    @api.multi
    @api.depends('invoice_ids', 'invoice_ids.state',
                 'invoice_ids.amount_total', 'invoice_ids.residual',
                 'invoice_ids.company_id.invoice_maturity_margin')
    def _compute_risk_invoice(self):
        max_date = self._max_risk_date_due()
        for partner in self:
            invoices = partner.invoice_ids.filtered(
                lambda x: x.state in ['draft', 'proforma', 'proforma2'])
            partner.risk_invoice_draft = sum(invoices.mapped('amount_total'))
            invoices = partner.invoice_ids.filtered(
                lambda x: x.state == 'open' and x.date_due >= max_date)
            partner.risk_invoice_open = sum(invoices.mapped('residual'))
            invoices = partner.invoice_ids.filtered(
                lambda x: x.state == 'open' and x.date_due < max_date)
            partner.risk_invoice_unpaid = sum(invoices.mapped('residual'))

    @api.multi
    @api.depends('credit', 'risk_invoice_open', 'risk_invoice_unpaid')
    def _compute_risk_account_amount(self):
        for partner in self:
            partner.risk_account_amount = (
                partner.credit - partner.risk_invoice_open -
                partner.risk_invoice_unpaid)

    @api.multi
    @api.depends(
        'risk_sale_order', 'eval_risk_sale_order', 'max_risk_sale_order',
        'risk_invoice_draft', 'eval_risk_invoice_draft',
        'max_risk_invoice_draft',
        'risk_invoice_open', 'eval_risk_invoice_open', 'max_risk_invoice_open',
        'risk_invoice_unpaid', 'eval_risk_invoice_unpaid',
        'max_risk_invoice_unpaid',
        'risk_account_amount', 'eval_risk_account_amount',
        'max_risk_account_amount')
    def _compute_risk_exception(self):
        risk_field_list = self._risk_field_list()
        for partner in self:
            amount = 0.0
            for risk_field in risk_field_list:
                field_value = getattr(partner, risk_field, 0.0)
                max_value = getattr(partner, 'max_%s' % risk_field, 0.0)
                if max_value and field_value > max_value:
                    partner.risk_exception = True
                if getattr(partner, 'eval_%s' % risk_field, False):
                    amount += field_value
            partner.risk_total = amount
            if amount > partner.credit_limit:
                partner.risk_exception = True

    @api.model
    def _max_risk_date_due(self):
        return fields.Date.to_string(datetime.today().date() - relativedelta(
            days=self.env.user.company_id.invoice_maturity_margin))

    @api.model
    def _risk_field_list(self):
        return ['risk_sale_order', 'risk_invoice_draft', 'risk_invoice_open',
                'risk_invoice_unpaid', 'risk_account_amount']
