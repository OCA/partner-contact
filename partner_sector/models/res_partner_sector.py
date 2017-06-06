# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# © 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, exceptions, models


class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Sector"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(comodel_name='res.partner.sector',
                                ondelete='restrict')
    child_ids = fields.One2many(comodel_name='res.partner.sector',
                                inverse_name='parent_id',
                                string="Children")
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(
                _('Error! You cannot create recursive sectors.'))
