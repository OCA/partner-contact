# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


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
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)

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
