# -*- coding: utf-8 -*-
# © 2014-2016 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    job_position_id = fields.Many2one(
        "res.partner.job_position",
        "Categorized job position",
        oldname="job_position")


class ResPartnerJobPosition(models.Model):
    _name = "res.partner.job_position"
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Job position"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(
        "res.partner.job_position",
        "Parent", ondelete='restrict')
    child_ids = fields.One2many(
        "res.partner.job_position",
        "parent_id",
        "Children",
        oldname="children")
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error! You cannot create recursive job positions.'))
