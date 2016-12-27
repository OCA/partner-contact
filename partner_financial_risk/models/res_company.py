# -*- coding: utf-8 -*-
# Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_unpaid_margin = fields.Integer(
        string="Maturity Margin",
        help="Days after due date to set an invoice as unpaid")
