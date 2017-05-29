# -*- coding: utf-8 -*-
# © 2014-2015 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
        "Child departments")
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error! You cannot create recursive departments.'))
