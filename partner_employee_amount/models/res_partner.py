# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Antonio Espinosa
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_amount = fields.Integer(
        oldname="employees_number")
    employee_amount_range_id = fields.Many2one(
        "res.partner.employee_amount_range",
        "Employee amount range",
        help="Range of this partner depending on the employee amount.",
        oldname="employees_range")


class ResPartnerEmployeeAmountRange(models.Model):
    _name = "res.partner.employee_amount_range"
    _description = "Partner employee amount range"

    name = fields.Char(required=True, translate=True)
