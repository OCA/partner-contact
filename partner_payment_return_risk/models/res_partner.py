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
        compute='_compute_risk_payment_return', store=True,
        string='Total Returned Invoices',
        help='Total returned invoices in Open state')

    @api.multi
    @api.depends('invoice_ids.state', 'invoice_ids.returned_payment')
    def _compute_risk_payment_return(self):
        AccountInvoice = self.env['account.invoice']
        for partner in self:
            partner.risk_payment_return = AccountInvoice.read_group(
                [('partner_id', '=', partner.id),
                 ('returned_payment', '=', True),
                 ('state', '=', 'open'),
                 ],
                ['residual'],
                []
            )[0]['residual']

    @api.model
    def _risk_field_list(self):
        res = super(ResPartner, self)._risk_field_list()
        res.append(('risk_payment_return', 'risk_payment_return_limit',
                    'risk_payment_return_include'))
        return res
