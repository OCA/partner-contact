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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, values):
        for record in self:
            values = record._add_revision(values)
        return super(ResPartner, self).write(values)

    @api.multi
    def _add_revision(self, values):
        """ Add a revision on a partner

        By default, when a partner is modified by a user or by the
        system, the changes are applied and a validated revision is
        created.  Callers which want to delegate the write of some
        fields to the revision must explicitly ask for it by providing a
        key ``__revision_rules`` in the environment's context.

        :param values: the values being written on the partner
        :type values: dict

        :returns: dict of values that should be wrote on the partner
        (fields with a 'Validate' or 'Never' rule are excluded)

        """
        self.ensure_one()
        write_values = values.copy()
        changes = []
        rules = self.env['revision.behavior'].get_rules(self._model._name)
        for field in values:
            rule = rules.get(field)
            if not rule:
                continue
            if field in values:
                if self[field] == values[field]:
                    # TODO handle relations, types
                    continue
                change = {
                    'current_value': self[field],
                    'new_value': values[field],
                    'field_id': rule.field_id.id,
                }
                if not self.env.context.get('__revision_rules'):
                    # by default always write on partner
                    change['state'] = 'done'
                elif rule.default_behavior == 'auto':
                    change['state'] = 'done'
                elif rule.default_behavior == 'validate':
                    change['state'] = 'draft'
                    write_values.pop(field)  # change to apply manually
                elif rule.default_behavior == 'never':
                    change['state'] = 'cancel'
                    write_values.pop(field)  # change never applied
            changes.append(change)
        if changes:
            self.env['res.partner.revision'].create({
                'partner_id': self.id,
                'change_ids': [(0, 0, vals) for vals in changes],
                'date': fields.Datetime.now(),
            })
        return write_values
