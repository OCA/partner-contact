# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Antonio Espinosa
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResPartnerNuts(models.Model):
    _name = 'res.partner.nuts'
    _order = "parent_left"
    _parent_order = "name"
    _parent_store = True
    _description = "NUTS Item"

    # NUTS fields
    level = fields.Integer(required=True)
    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    country_id = fields.Many2one(comodel_name='res.country', string="Country",
                                 required=True)
    state_id = fields.Many2one(comodel_name='res.country.state',
                               string='State')
    # Parent hierarchy
    parent_id = fields.Many2one(comodel_name='res.partner.nuts',
                                ondelete='restrict')
    child_ids = fields.One2many(
        'res.partner.nuts',
        'parent_id',
        "Children",
        oldname="children")
    parent_left = fields.Integer('Parent Left', select=True)
    parent_right = fields.Integer('Parent Right', select=True)
