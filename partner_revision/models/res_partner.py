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
        if self.env.context.get('__no_revision'):
            return super(ResPartner, self).write(values)
        else:
            for record in self:
                values = record._add_revision(values)
                super(ResPartner, record).write(values)
        return True

    @api.multi
    def _has_field_changed(self, field, value):
        self.ensure_one()
        field_def = self._fields[field]
        return field_def.convert_to_write(self[field]) != value

    @api.multi
    def convert_field_for_revision(self, field, value):
        field_def = self._fields[field]
        if field_def.type == 'many2one':
            # store as 'reference'
            comodel = field_def.comodel_name
            return "%s,%s" % (comodel, value) if value else False
        else:
            return value

    @api.multi
    def _prepare_revision_change(self, rule, field, value):
        """ Prepare data for a revision change

        It returns a dict of the values to write on the revision change
        and a boolean that indicates if the value should be popped out
        of the values to write on the model.

        :returns: dict of values, boolean
        """
        field_def = self._fields[field]
        # get a ready to write value for the type of the field,
        # for instance takes '.id' from a many2one's record (the
        # new value is already a value as expected for the
        # write)
        current_value = field_def.convert_to_write(self[field])
        # get values ready to write as expected by the revision
        # (for instance, a many2one is written in a reference
        # field)
        current_value = self.convert_field_for_revision(field,
                                                        current_value)
        new_value = self.convert_field_for_revision(field, value)
        change = {
            'current_value': current_value,
            'new_value': new_value,
            'field_id': rule.field_id.id,
        }
        pop_value = False
        if not self.env.context.get('__revision_rules'):
            # by default always write on partner
            change['state'] = 'done'
        elif rule.default_behavior == 'auto':
            change['state'] = 'done'
        elif rule.default_behavior == 'validate':
            change['state'] = 'draft'
            pop_value = True  # change to apply manually
        elif rule.default_behavior == 'never':
            change['state'] = 'cancel'
            pop_value = True  # change never applied
        return change, pop_value

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
                if not self._has_field_changed(field, values[field]):
                    continue
            change, pop_value = self._prepare_revision_change(
                rule, field, values[field]
            )
            if pop_value:
                write_values.pop(field)
            changes.append(change)
        if changes:
            self.env['res.partner.revision'].create({
                'partner_id': self.id,
                'change_ids': [(0, 0, vals) for vals in changes],
                'date': fields.Datetime.now(),
            })
        return write_values
