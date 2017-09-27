# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    risk_payment_return_include = fields.Boolean(
        string='Include Payments Returns', help='Full risk computation')
    risk_payment_return_limit = fields.Monetary(
        string='Limit Payments Returns', help='Set 0 if it is not locked')
    risk_payment_return = fields.Monetary(
        compute='_compute_risk_invoice', store=True,
        string='Total Returned Invoices',
        help='Total returned invoices in Open state')

    @api.model
    def _risk_invoice_domain_list(self):
        res = super(ResPartner, self)._risk_invoice_domain_list()
        for reg in res:
            reg['domain'].append(('returned_payment', '=', False))
        res.append({
            'risk_field': 'risk_payment_return',
            'domain': [('returned_payment', '=', True)],
            'amount_field': 'residual_signed'
        })
        return res

    @api.model
    def _risk_invoice_depends_fields(self):
        res = super(ResPartner, self)._risk_invoice_depends_fields()
        res.extend([
            'invoice_ids.returned_payment',
            'child_ids.invoice_ids.returned_payment',
        ])
        return res

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_payment_return', 'risk_payment_return_limit',
                    'risk_payment_return_include'))
        return res

    # TODO: Avoid overwrite function
    @api.multi
    @api.depends('credit', 'risk_invoice_open', 'risk_invoice_unpaid',
                 'child_ids.credit', 'child_ids.risk_invoice_open',
                 'child_ids.risk_invoice_unpaid')
    def _compute_risk_account_amount(self):
        for partner in self.filtered(lambda x: x.customer and not x.parent_id):
            partner.risk_account_amount = (
                partner.credit - partner.risk_invoice_open -
                partner.risk_invoice_unpaid - partner.risk_payment_return)
