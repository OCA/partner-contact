# -*- coding: utf-8 -*-
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    department_id = fields.Many2one(
        "res.partner.department",
        "Department",
        oldname="department")


class ResPartnerDepartment(models.Model):
    _name = 'res.partner.department'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Department"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(
        "res.partner.department",
        "Parent department",
        ondelete='restrict')
    child_ids = fields.One2many(
        "res.partner.department",
        "parent_id",
        "Child departments",
        oldname="children")
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
