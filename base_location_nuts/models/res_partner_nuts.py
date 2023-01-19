# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerNuts(models.Model):
    _name = 'res.partner.nuts'
    _order = 'parent_left'
    _parent_order = 'name'
    _parent_store = True
    _description = 'NUTS Item'

    # NUTS fields
    level = fields.Integer(required=True)
    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    country_id = fields.Many2one(comodel_name='res.country', string='Country',
                                 required=True)
    state_id = fields.Many2one(comodel_name='res.country.state',
                               string='State')
    # Parent hierarchy
    parent_id = fields.Many2one(comodel_name='res.partner.nuts',
                                ondelete='restrict')
    child_ids = fields.One2many(comodel_name='res.partner.nuts',
                                inverse_name='parent_id', string='Children',
                                oldname='children')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
