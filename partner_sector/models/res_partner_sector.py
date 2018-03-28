# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# © 2016 Tecnativa S.L. - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, exceptions, models


class ResPartnerSector(models.Model):
    _name = 'res.partner.sector'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "Sector"

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one(string='Parent',
                                comodel_name='res.partner.sector',
                                ondelete='restrict')
    child_ids = fields.One2many(comodel_name='res.partner.sector',
                                inverse_name='parent_id',
                                string="Children")
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
    complete_name = fields.Char(
        string="Complete Name",
        compute='_compute_complete_name',
        store=True,
    )

    @api.multi
    @api.depends("name", "parent_id", "parent_id.name")
    def _compute_complete_name(self):
        for rec in self:
            rec.complete_name = rec.display_name

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name or '/')
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise exceptions.ValidationError(
                _('Error! You cannot create recursive sectors.'))
