# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

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
        string='Include Unpaid Invoices', help='Full risk computation')
    risk_invoice_unpaid_limit = fields.Monetary(
        string='Limit In Unpaid Invoices', help='Set 0 if it is not locked')
    risk_invoice_unpaid = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Unpaid Invoices',
        help='Residual amount of invoices in Open state and the date due is '
             'exceeded, considering Unpaid Margin set in account settings')

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

    @api.model
    def _risk_invoice_domain_list(self):
        max_date = self._max_risk_date_due()
        return [
            {'risk_field': 'risk_invoice_draft',
             'domain': [('state', 'in', ['draft', 'proforma', 'proforma2'])],
             'amount_field': 'amount_total'},
            {'risk_field': 'risk_invoice_open',
             'domain': [('state', '=', 'open'), ('date_due', '>=', max_date)],
             'amount_field': 'residual_signed'},
            {'risk_field': 'risk_invoice_unpaid',
             'domain': [('state', '=', 'open'), '|',
                        ('date_due', '=', False), ('date_due', '<', max_date)],
             'amount_field': 'residual_signed'},
        ]

    @api.model
    def _risk_invoice_depends_fields(self):
        return [
            'invoice_ids', 'invoice_ids.state',
            'invoice_ids.amount_total', 'invoice_ids.residual_signed',
            'invoice_ids.company_id.invoice_unpaid_margin',
            'child_ids.invoice_ids', 'child_ids.invoice_ids.state',
            'child_ids.invoice_ids.amount_total',
            'child_ids.invoice_ids.residual_signed',
            'child_ids.invoice_ids.company_id.invoice_unpaid_margin',
        ]

    @api.multi
    @api.depends(lambda x: x._risk_invoice_depends_fields())
    def _compute_risk_invoice(self):
        def sum_group(group, field):
            return sum([x[field] for x in group if
                        x['partner_id'][0] in partner_ids])
        customers = self.filtered('customer')
        if not customers:
            return  # pragma: no cover
        AccountInvoice = self.env['account.invoice']
        partners = customers | customers.mapped('child_ids')
        domain = [('type', 'in', ['out_invoice', 'out_refund']),
                  ('partner_id', 'in', partners.ids)]
        groups = {}
        amount_fields = {}
        for risk_dic in self._risk_invoice_domain_list():
            groups[risk_dic['risk_field']] = AccountInvoice.read_group(
                domain + risk_dic['domain'],
                ['partner_id', risk_dic['amount_field']],
                ['partner_id'])
            amount_fields[risk_dic['risk_field']] = risk_dic['amount_field']
        for partner in customers:
            partner_ids = (partner | partner.child_ids).ids
            partner_vals = {}
            for risk_field in groups.keys():
                partner_vals[risk_field] = sum_group(
                    groups[risk_field], amount_fields[risk_field])
            partner.update(partner_vals)

    @api.multi
    @api.depends('credit', 'risk_invoice_open', 'risk_invoice_unpaid',
                 'child_ids.credit', 'child_ids.risk_invoice_open',
                 'child_ids.risk_invoice_unpaid')
    def _compute_risk_account_amount(self):
        for partner in self.filtered(lambda x: x.customer and not x.parent_id):
            partner.risk_account_amount = (
                partner.credit - partner.risk_invoice_open -
                partner.risk_invoice_unpaid)

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
        invoices = self.env['account.invoice'].search([
            ('date_due', '>=', last_check), ('date_due', '<', max_date)])
        invoices.mapped('partner_id')._compute_risk_invoice()
        ConfigParameter.set_param(
            'partner_financial_risk.last_check', max_date)
        return True
