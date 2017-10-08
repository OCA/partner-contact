# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_payment_return_include = fields.Boolean(
        string='Include Payments Returns',
        help='Full risk computation.\n'
             'Residual amount of move lines not reconciled with returned '
             'lines related.')
    risk_payment_return_limit = fields.Monetary(
        string='Limit Payments Returns', help='Set 0 if it is not locked')
    risk_payment_return = fields.Monetary(
        compute='_compute_risk_account_amount', store=True,
        string='Total Payments Returns',
        help='Residual amount of move lines not reconciled with returned '
             'lines related.')

    @api.model
    def _risk_account_groups(self):
        res = super(ResPartner, self)._risk_account_groups()
        res['open']['domain'] += [
            ('partial_reconcile_returned_ids', '=', False),
        ]
        res['unpaid']['domain'] += [
            ('partial_reconcile_returned_ids', '=', False),
        ]
        res['returned'] = {
            'domain': [('reconciled', '=', False),
                       ('account_id.internal_type', '=', 'receivable'),
                       ('partial_reconcile_returned_ids', '!=', False)],
            'fields': ['partner_id', 'account_id', 'amount_residual'],
            'group_by': ['partner_id', 'account_id']
        }
        return res

    @api.multi
    def _prepare_risk_account_vals(self, groups):
        vals = super(ResPartner, self)._prepare_risk_account_vals(groups)
        vals['risk_payment_return'] = sum(
            reg['amount_residual'] for reg in groups['returned']['read_group']
            if reg['partner_id'][0] == self.id)
        return vals

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_payment_return', 'risk_payment_return_limit',
                    'risk_payment_return_include'))
        return res
