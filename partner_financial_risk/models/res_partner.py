# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    move_line_ids = fields.One2many(
        comodel_name='account.move.line',
        inverse_name='partner_id',
        string='Account Moves'
    )
    risk_invoice_draft_include = fields.Boolean(
        string='Include Draft Invoices', help='Full risk computation')
    risk_invoice_draft_limit = fields.Monetary(
        string='Limit In Draft Invoices', help='Set 0 if it is not locked')
    risk_invoice_draft = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Draft Invoices',
        help='Total amount of invoices in Draft or Pro-forma state')

    risk_invoice_open_include = fields.Boolean(
        string='Include Open Invoices/Principal Balance',
        help='Full risk computation.\n'
             'Residual amount of move lines not reconciled with the same '
             'account that is set as partner receivable and date maturity '
             'not exceeded, considering Due Margin set in account settings.')
    risk_invoice_open_limit = fields.Monetary(
        string='Limit In Open Invoices/Principal Balance',
        help='Set 0 if it is not locked')
    risk_invoice_open = fields.Monetary(
        compute='_compute_risk_account_amount', store=True,
        string='Total Open Invoices/Principal Balance',
        help='Residual amount of move lines not reconciled with the same '
             'account that is set as partner receivable and date maturity '
             'not exceeded, considering Due Margin set in account settings.')
    risk_invoice_unpaid_include = fields.Boolean(
        string='Include Unpaid Invoices/Principal Balance',
        help='Full risk computation.\n'
             'Residual amount of move lines not reconciled with the same '
             'account that is set as partner receivable and date maturity '
             'exceeded, considering Due Margin set in account settings.')
    risk_invoice_unpaid_limit = fields.Monetary(
        string='Limit In Unpaid Invoices/Principal Balance',
        help='Set 0 if it is not locked')
    risk_invoice_unpaid = fields.Monetary(
        compute='_compute_risk_account_amount', store=True,
        string='Total Unpaid Invoices/Principal Balance',
        help='Residual amount of move lines not reconciled with the same '
             'account that is set as partner receivable and date maturity '
             'exceeded, considering Due Margin set in account settings.')

    risk_account_amount_include = fields.Boolean(
        string='Include Other Account Open Amount',
        help='Full risk computation.\n'
             'Residual amount of move lines not reconciled with distinct '
             'account that is set as partner receivable and date maturity '
             'not exceeded, considering Due Margin set in account settings.')
    risk_account_amount_limit = fields.Monetary(
        string='Limit Other Account Open Amount',
        help='Set 0 if it is not locked')
    risk_account_amount = fields.Monetary(
        compute='_compute_risk_account_amount', store=True,
        string='Total Other Account Open Amount',
        help='Residual amount of move lines not reconciled with distinct '
             'account that is set as partner receivable and date maturity '
             'not exceeded, considering Due Margin set in account settings.')
    risk_account_amount_unpaid_include = fields.Boolean(
        string='Include Other Account Unpaid Amount',
        help='Full risk computation.\n'
             'Residual amount of move lines not reconciled with distinct '
             'account that is set as partner receivable and date maturity '
             'exceeded, considering Due Margin set in account settings.')
    risk_account_amount_unpaid_limit = fields.Monetary(
        string='Limit Other Account Unpaid Amount',
        help='Set 0 if it is not locked')
    risk_account_amount_unpaid = fields.Monetary(
        compute='_compute_risk_account_amount', store=True,
        string='Total Other Account Unpaid Amount',
        help='Residual amount of move lines not reconciled with distinct '
             'account that is set as partner receivable and date maturity '
             'exceeded, considering Due Margin set in account settings.')

    risk_total = fields.Monetary(
        compute='_compute_risk_exception',
        string='Total Risk', help='Sum of total risk included')
    risk_exception = fields.Boolean(
        compute='_compute_risk_exception',
        string='Risk Exception',
        help='It Indicate if partner risk exceeded')
    credit_policy = fields.Char()
    risk_allow_edit = fields.Boolean(compute='_compute_risk_allow_edit')
    credit_limit = fields.Float(track_visibility='onchange')

    @api.multi
    def _compute_risk_allow_edit(self):
        is_editable = self.env.user.has_group(
            'base.group_sale_manager') or self.env.user.has_group(
            'account.group_account_manager')
        for partner in self.filtered('customer'):
            partner.risk_allow_edit = is_editable

    @api.multi
    @api.depends(
        'customer', 'invoice_ids', 'invoice_ids.state',
        'invoice_ids.amount_total',
        'child_ids.invoice_ids', 'child_ids.invoice_ids.state',
        'child_ids.invoice_ids.amount_total')
    def _compute_risk_invoice(self):
        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self.filtered('customer'):
            if not partner.id:
                continue
            all_partners_and_children[partner] = self.with_context(
                active_test=False).search([('id', 'child_of', partner.id)]).ids
            all_partner_ids += all_partners_and_children[partner]
        if not all_partner_ids:
            return
        total_group = self.env['account.invoice'].sudo().read_group(
            [('type', 'in', ['out_invoice', 'out_refund']),
             ('state', 'in', ['draft', 'proforma', 'proforma2']),
             ('partner_id', 'in', self.ids)],
            ['partner_id', 'amount_total'],
            ['partner_id'])
        for partner, child_ids in all_partners_and_children.items():
            partner.risk_invoice_draft = sum(
                x['amount_total']
                for x in total_group if x['partner_id'][0] in child_ids)

    @api.model
    def _risk_account_groups(self):
        max_date = self._max_risk_date_due()
        return {
            'open': {
                'domain': [('reconciled', '=', False),
                           ('account_id.internal_type', '=', 'receivable'),
                           ('date_maturity', '>=', max_date)],
                'fields': ['partner_id', 'account_id', 'amount_residual'],
                'group_by': ['partner_id', 'account_id']
            },
            'unpaid': {
                'domain': [('reconciled', '=', False),
                           ('account_id.internal_type', '=', 'receivable'),
                           ('date_maturity', '<', max_date)],
                'fields': ['partner_id', 'account_id', 'amount_residual'],
                'group_by': ['partner_id', 'account_id']
                }
        }

    @api.multi
    @api.depends('move_line_ids.amount_residual',
                 'move_line_ids.date_maturity',
                 'company_id.invoice_unpaid_margin')
    def _compute_risk_account_amount(self):
        AccountMoveLine = self.env['account.move.line'].sudo()
        customers = self.filtered(lambda x: x.customer and not x.parent_id)
        if not customers:
            return
        groups = self._risk_account_groups()
        for key, group in groups.iteritems():
            group['read_group'] = AccountMoveLine.read_group(
                group['domain'] + [('partner_id', 'in', customers.ids)],
                group['fields'],
                group['group_by'],
                lazy=False,
            )
        for partner in customers:
            partner.update(partner._prepare_risk_account_vals(groups))

    @api.multi
    def _prepare_risk_account_vals(self, groups):
        vals = {
            'risk_invoice_open': 0.0,
            'risk_invoice_unpaid': 0.0,
            'risk_account_amount': 0.0,
            'risk_account_amount_unpaid': 0.0,
        }
        for reg in groups['open']['read_group']:
            if reg['partner_id'][0] != self.id:
                continue
            if self.property_account_receivable_id.id == reg['account_id'][0]:
                vals['risk_invoice_open'] += reg['amount_residual']
            else:
                vals['risk_account_amount'] += reg['amount_residual']
        for reg in groups['unpaid']['read_group']:
            if reg['partner_id'][0] != self.id:
                continue  # pragma: no cover
            if self.property_account_receivable_id.id == reg['account_id'][0]:
                vals['risk_invoice_unpaid'] += reg['amount_residual']
            else:
                vals['risk_account_amount_unpaid'] += reg['amount_residual']
        return vals

    @api.multi
    @api.depends(lambda x: x._get_depends_compute_risk_exception())
    def _compute_risk_exception(self):
        risk_field_list = self._risk_field_list()
        for partner in self.filtered('customer'):
            amount = 0.0
            for risk_field in risk_field_list:
                field_value = getattr(partner, risk_field[0], 0.0)
                max_value = getattr(partner, risk_field[1], 0.0)
                if max_value and field_value > max_value:
                    partner.risk_exception = True
                if getattr(partner, risk_field[2], False):
                    amount += field_value
            partner.risk_total = amount
            if partner.credit_limit and amount > partner.credit_limit:
                partner.risk_exception = True

    @api.model
    def _max_risk_date_due(self):
        return fields.Date.to_string(datetime.today().date() - relativedelta(
            days=self.env.user.company_id.invoice_unpaid_margin))

    @api.model
    def _risk_field_list(self):
        return [
            ('risk_invoice_draft', 'risk_invoice_draft_limit',
             'risk_invoice_draft_include'),
            ('risk_invoice_open', 'risk_invoice_open_limit',
             'risk_invoice_open_include'),
            ('risk_invoice_unpaid', 'risk_invoice_unpaid_limit',
             'risk_invoice_unpaid_include'),
            ('risk_account_amount', 'risk_account_amount_limit',
             'risk_account_amount_include'),
            ('risk_account_amount_unpaid', 'risk_account_amount_unpaid_limit',
             'risk_account_amount_unpaid_include'),
        ]

    @api.model
    def _get_depends_compute_risk_exception(self):
        res = []
        for x in self._risk_field_list():
            res.extend((x[0], x[1], x[2], 'child_ids.%s' % x[0],
                        'child_ids.%s' % x[1], 'child_ids.%s' % x[2]))
        res.extend(('credit_limit', 'child_ids.credit_limit'))
        return res

    @api.model
    def process_unpaid_invoices(self):
        max_date = self._max_risk_date_due()
        ConfigParameter = self.env['ir.config_parameter']
        last_check = ConfigParameter.get_param(
            'partner_financial_risk.last_check', default='2016-01-01')
        move_lines = self.env['account.move.line'].search([
            ('reconciled', '=', False),
            ('account_id.internal_type', '=', 'receivable'),
            ('date_maturity', '>=', last_check),
            ('date_maturity', '<', max_date)])
        move_lines.mapped('partner_id')._compute_risk_account_amount()
        ConfigParameter.set_param(
            'partner_financial_risk.last_check', max_date)
        return True
