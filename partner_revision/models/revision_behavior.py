# -*- coding: utf-8 -*-
#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, fields, api


class RevisionBehavior(models.Model):
    _name = 'revision.behavior'
    _description = 'Revision Behavior'
    _rec_name = 'field_id'

    model_id = fields.Many2one(comodel_name='ir.model',
                               string='Model',
                               ondelete='cascade',
                               default=lambda self: self._default_model_id())
    field_id = fields.Many2one(comodel_name='ir.model.fields',
                               string='Field',
                               ondelete='cascade')
    default_behavior = fields.Selection(
        selection='_selection_default_behavior',
        string='Default Behavior',
        help="Auto: always apply a change.\n"
             "Validate: manually applied by an administrator.\n"
             "Never: change never applied.",
    )

    @api.model
    def _default_model_id(self):
        return self.env.ref('base.model_res_partner').id

    @api.model
    def _selection_default_behavior(self):
        return [('auto', 'Auto'),
                ('validate', 'Validate'),
                ('never', 'Never'),
                ]

    # TODO: cache
    @api.model
    def get_rules(self, model_name):
        rules = self.search([('model_id', '=', model_name)])
        return {rule.field_id.name: rule for rule in rules}
