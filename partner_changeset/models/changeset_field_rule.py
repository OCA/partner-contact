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
from openerp.tools.cache import ormcache


class ChangesetFieldRule(models.Model):
    _name = 'changeset.field.rule'
    _description = 'Changeset Field Rules'
    _rec_name = 'field_id'

    model_id = fields.Many2one(comodel_name='ir.model',
                               string='Model',
                               ondelete='cascade',
                               default=lambda self: self._default_model_id())
    field_id = fields.Many2one(comodel_name='ir.model.fields',
                               string='Field',
                               ondelete='cascade')
    action = fields.Selection(
        selection='_selection_action',
        string='Action',
        help="Auto: always apply a change.\n"
             "Validate: manually applied by an administrator.\n"
             "Never: change never applied.",
    )

    _sql_constraints = [
        ('model_field_uniq',
         'unique (model_id, field_id)',
         'A rule already exists for this field.')
    ]

    @api.model
    def _default_model_id(self):
        return self.env.ref('base.model_res_partner').id

    @api.model
    def _selection_action(self):
        return [('auto', 'Auto'),
                ('validate', 'Validate'),
                ('never', 'Never'),
                ]

    @ormcache()
    @api.model
    def get_rules(self, model_name):
        rules = self.search([('model_id', '=', model_name)])
        return {rule.field_id.name: rule for rule in rules}

    @api.model
    def create(self, vals):
        record = super(ChangesetFieldRule, self).create(vals)
        self.clear_caches()
        return record

    @api.multi
    def write(self, vals):
        result = super(ChangesetFieldRule, self).write(vals)
        self.clear_caches()
        return result

    @api.multi
    def unlink(self):
        result = super(ChangesetFieldRule, self).unlink()
        self.clear_caches()
        return result
