# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_unpaid_margin = fields.Integer(
        string="Maturity Margin",
        help="Days after due date to set an invoice as unpaid."
             "The change of this field recompute all partners risk,"
             "be patient.")

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        if 'invoice_unpaid_margin' in vals:
            self.env['res.partner'].search(
                [('customer', '=', True)])._compute_risk_invoice()
        return res
