# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartnerLAU(models.Model):
    _name = 'res.partner.lau'
    _order = "code"
    _parent_order = "name"
    _parent_store = True
    _description = "LAU Item"

    level = fields.Integer(required=True, index=True)
    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    country_id = fields.Many2one('res.country', 'Country', required=True)
    state_id = fields.Many2one('res.country.state', 'State')
    # Parent hierarchy
    parent_id = fields.Many2one('res.partner.lau', ondelete='restrict')
    child_ids = fields.One2many('res.partner.lau', 'parent_id', 'Children')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
