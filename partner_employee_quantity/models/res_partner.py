# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2015 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    employee_quantity = fields.Integer()
    employee_quantity_range_id = fields.Many2one(
        comodel_name="res.partner.employee_quantity_range",
        string="Employee quantity range",
        help="Range of this partner depending on the employee quantity.",
    )


class ResPartnerEmployeeQuantityRange(models.Model):
    _name = "res.partner.employee_quantity_range"
    _description = "Partner employee quantity range"

    name = fields.Char(required=True, translate=True)
