# -*- coding: utf-8 -*-
# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_quantity = fields.Integer(
        oldname="employees_number")
    employee_quantity_range_id = fields.Many2one(
        "res.partner.employee_quantity_range",
        "Employee quantity range",
        help="Range of this partner depending on the employee quantity.",
        oldname="employees_range")


class ResPartnerEmployeeQuantityRange(models.Model):
    _name = "res.partner.employee_quantity_range"
    _description = "Partner employee quantity range"

    name = fields.Char(required=True, translate=True)
