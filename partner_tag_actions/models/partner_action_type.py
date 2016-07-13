# -*- coding: utf-8 -*-
# Copyright 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class PartnerActionType(models.Model):
    _name = 'partner.action.type'
    _description = 'Partner Action Type'
    _order = 'priority'

    name = fields.Char('Name', translate=True, required=True)
    priority = fields.Integer('Priority', required=True, default=0)
    is_active = fields.Boolean('Active', default=True)

    add_tag = fields.Many2one('res.partner.category', required=False,
                              string='Add Tag')
    remove_tag = fields.Many2one('res.partner.category', required=False,
                                 string='Remove Tag')

    @api.model
    def get_default(self):
        return self.search([('is_active', '=', True)], limit=1).id
