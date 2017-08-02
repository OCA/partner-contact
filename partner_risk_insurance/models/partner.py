# -*- coding: utf-8 -*-
# Copyright 2014 AvancOSC - Daniel Campos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    company_credit_limit = fields.Float(
        string='Company\'s Credit Limit',
        help='Credit limit granted by the company.',
    )
    insurance_credit_limit = fields.Float(
        string='Insurance\'s Credit Limit',
        help='Credit limit granted by the insurance company.',
    )
    risk_insurance_coverage_percent = fields.Float(
        string='Insurance\'s Credit Coverage',
        help='Percentage of the credit covered by the insurance.',
    )
    risk_insurance_requested = fields.Boolean(
        string='Insurance Requested',
        help='Mark this field if an insurance was requested for the credit of '
             'this partner.',
    )
    risk_insurance_grant_date = fields.Date(
        string='Insurance Grant Date',
        help='Date when the insurance was granted by the insurance company.',
    )
    risk_insurance_code = fields.Char(
        string='Insurance Code',
        help='Code assigned to this partner by the risk insurance company.',
    )
    risk_insurance_code_2 = fields.Char(
        string='Insurance Code 2',
        help='Secondary code assigned to this partner by the risk insurance '
             'company.',
    )

    @api.onchange('insurance_credit_limit', 'company_credit_limit')
    def _onchage_insurance_credit_limit(self):
        self.ensure_one()
        self.credit_limit = (self.insurance_credit_limit +
                             self.company_credit_limit)
