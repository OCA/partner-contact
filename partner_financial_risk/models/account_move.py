# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def write(self, vals):
        res = super(AccountMoveLine, self).write(vals)
        if 'date_maturity' in vals:
            self.mapped('partner_id')._compute_risk_invoice()
        return res
