# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    risk_invoice_draft_include = fields.Boolean(
        string='Include Draft Invoices', help='Full risk computation')
    risk_invoice_draft_limit = fields.Monetary(
        string='Limit In Draft Invoices', help='Set 0 if it is not locked')
    risk_invoice_draft = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Draft Invoices',
        help='Total amount of invoices in Draft or Pro-forma state')
    risk_invoice_open_include = fields.Boolean(
        string='Include Open Invoices', help='Full risk computation')
    risk_invoice_open_limit = fields.Monetary(
        string='Limit In Open Invoices', help='Set 0 if it is not locked')
    risk_invoice_open = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Open Invoices',
        help='Residual amount of invoices in Open state and the date due is '
             'not exceeded, considering Due Margin set in account '
             'settings')
    risk_invoice_unpaid_include = fields.Boolean(
        string='Include Due Invoices', help='Full risk computation')
    risk_invoice_unpaid_limit = fields.Monetary(
        string='Limit In Due Invoices', help='Set 0 if it is not locked')
    risk_invoice_unpaid = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Due Invoices',
        help='Residual amount of invoices in Open state and the date due is '
             'exceeded, considering Due Margin set in account settings')

    risk_account_amount_include = fields.Boolean(
        string='Include Other Account Amount', help='Full risk computation')
    risk_account_amount_limit = fields.Monetary(
        string='Limit Other Account Amount', help='Set 0 if it is not locked')
    risk_account_amount = fields.Monetary(
        compute='_compute_risk_account_amount',
        string='Other Account Amount',
        help='Difference between accounting credit and rest of totals')

    risk_total = fields.Monetary(
        compute='_compute_risk_exception',
        string='Total Risk', help='Sum of total risk included')
    risk_exception = fields.Boolean(
        compute='_compute_risk_exception',
        string='Risk Exception',
        help='It Indicate if partner risk exceeded')

    @api.multi
    @api.depends('sale_order_ids', 'sale_order_ids.invoice_pending_amount')
    def _compute_risk_sale_order(self):
        for partner in self:
            partner.risk_sale_order = sum(
                partner.sale_order_ids.mapped('invoice_pending_amount'))

    @api.multi
    @api.depends('invoice_ids', 'invoice_ids.state',
                 'invoice_ids.amount_total', 'invoice_ids.residual',
                 'invoice_ids.company_id.invoice_due_margin')
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
    @api.depends('risk_sale_order', 'risk_sale_order_include',
                 'risk_sale_order_limit',
                 'risk_invoice_draft', 'risk_invoice_draft_include',
                 'risk_invoice_draft_limit', 'risk_invoice_open',
                 'risk_invoice_open_include', 'risk_invoice_open_limit',
                 'risk_invoice_unpaid', 'risk_invoice_unpaid_include',
                 'risk_invoice_unpaid_limit', 'risk_account_amount',
                 'risk_account_amount_include', 'risk_account_amount_limit',
                 'credit_limit')
    # @api.depends(lambda x: x._depends_list)
    def _compute_risk_exception(self):
        risk_field_list = self._risk_field_list()
        for partner in self:
            amount = 0.0
            for risk_field in risk_field_list:
                field_value = getattr(partner, risk_field[0], 0.0)
                max_value = getattr(partner, risk_field[1], 0.0)
                if max_value and field_value > max_value:
                    partner.risk_exception = True
                if getattr(partner, risk_field[2], False):
                    amount += field_value
            partner.risk_total = amount
            if amount > partner.credit_limit:
                partner.risk_exception = True

    @api.model
    def _max_risk_date_due(self):
        return fields.Date.to_string(datetime.today().date() - relativedelta(
            days=self.env.user.company_id.invoice_due_margin))

    @api.model
    def _risk_field_list(self):
        return [
            ('risk_sale_order', 'risk_sale_order_limit',
            'risk_sale_order_include'),
            ('risk_invoice_draft', 'risk_invoice_draft_limit',
            'risk_invoice_draft_include'),
            ('risk_invoice_open', 'risk_invoice_open_limit',
             'risk_invoice_open_include'),
            ('risk_invoice_unpaid', 'risk_invoice_unpaid_limit',
            'risk_invoice_unpaid_include'),
            ('risk_account_amount', 'risk_account_amount_limit',
             'risk_account_amount_include'),
        ]

    @api.model
    def _depends_list(self):
        ss = (
            'risk_sale_order', 'risk_sale_order_include', 'risk_sale_order_limit',
            'risk_invoice_draft', 'risk_invoice_draft_include',
            'risk_invoice_draft_limit', 'risk_invoice_open',
            'risk_invoice_open_include', 'risk_invoice_open_limit',
            'risk_invoice_unpaid', 'risk_invoice_unpaid_include',
            'risk_invoice_unpaid_limit', 'risk_account_amount',
            'risk_account_amount_include', 'risk_account_amount_limit',
            'credit_limit')
        return ss