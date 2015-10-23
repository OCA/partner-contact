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
    source_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Source Model',
        ondelete='cascade',
        domain=lambda self: [('id', 'in', self._domain_source_models().ids)],
        help="If a source model is defined, the rule will be applied only "
             "when the change is made from this origin.  "
             "Rules without source model are global and applies to all "
             "backends.\n"
             "Rules with a source model have precedence over global rules, "
             "but if a field has no rule with a source model, the global rule "
             "is used."
    )

    _sql_constraints = [
        ('model_field_uniq',
         'unique (model_id, source_model_id, field_id)',
         'A rule already exists for this field.'),
    ]

    @api.model
    def _domain_source_models(self):
        """ Returns the models for which we can define rules.

        Example for submodules (replace by the xmlid of the model):

        ::
            models = super(ChangesetFieldRule, self)._domain_source_models()
            return models | self.env.ref('base.model_res_users')

        Rules without model are global and apply for all models.

        """
        return self.env.ref('base.model_res_users')

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
    def get_rules(self, model_name, source_model_name):
        """ Return the rules for a model

        When a model is specified, it will return the rules for this
        model.  Fields that have no rule for this model will use the
        global rules (those without source).

        The source model is the model which ask for a change, it will be
        for instance ``res.users``, ``lefac.backend`` or
        ``magellan.backend``.

        The second argument (``source_model_name``) is optional but
        cannot be an optional keyword argument otherwise it would not be
        in the key for the cache. The callers have to pass ``None`` if
        they want only global rules.
        """
        model_rules = self.search(
            [('model_id', '=', model_name),
             '|', ('source_model_id.model', '=', source_model_name),
                  ('source_model_id', '=', False)],
            # using 'DESC' means that 'NULLS FIRST' is the default
            order='source_model_id DESC',
        )
        # model's rules have precedence over global ones so we iterate
        # over global rules first, then we update them with the rules
        # which have a source model
        return {rule.field_id.name: rule for rule in model_rules}

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
