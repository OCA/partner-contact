# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartnerNace(models.Model):
    _name = 'res.partner.nace'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "NACE Activity"

    level = fields.Integer(required=True)
    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    generic = fields.Char(string="ISIC Rev.4")
    rules = fields.Text()
    central_content = fields.Text(translate=True, string="Contents")
    limit_content = fields.Text(translate=True, string="Also contents")
    exclusions = fields.Char(string="Excludes")
    parent_id = fields.Many2one(comodel_name='res.partner.nace',
                                ondelete='restrict')
    child_ids = fields.One2many(comodel_name='res.partner.nace',
                                inverse_name='parent_id', string="Children")
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
