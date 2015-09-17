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


class ResPartnerRevision(models.Model):
    _name = 'res.partner.revision'
    _description = 'Partner Revision'
    _order = 'date desc'
    _rec_name = 'date'

    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner',
                                 required=True)
    change_ids = fields.One2many(comodel_name='res.partner.revision.change',
                                 inverse_name='revision_id',
                                 string='Changes')
    date = fields.Datetime(default=fields.Datetime.now)
    note = fields.Text()

    @api.multi
    def apply(self):
        self.mapped('change_ids').apply()


class ResPartnerRevisionChange(models.Model):
    _name = 'res.partner.revision.change'
    _description = 'Partner Revision Change'
    _rec_name = 'field_id'

    revision_id = fields.Many2one(comodel_name='res.partner.revision',
                                  required=True,
                                  string='Revision',
                                  ondelete='cascade')
    field_id = fields.Many2one(comodel_name='ir.model.fields',
                               string='Field',
                               required=True)

    current_value_char = fields.Char(string='Current')
    current_value_date = fields.Date(string='Current')
    current_value_datetime = fields.Datetime(string='Current')
    current_value_float = fields.Float(string='Current')
    current_value_integer = fields.Integer(string='Current')
    current_value_text = fields.Text(string='Current')
    current_value_boolean = fields.Boolean(string='Current')
    current_value_reference = fields.Reference(string='Current',
                                               selection='_reference_models')

    new_value_char = fields.Char(string='New')
    new_value_date = fields.Date(string='New')
    new_value_datetime = fields.Datetime(string='New')
    new_value_float = fields.Float(string='New')
    new_value_integer = fields.Integer(string='New')
    new_value_text = fields.Text(string='New')
    new_value_boolean = fields.Boolean(string='New')
    new_value_reference = fields.Reference(string='New',
                                           selection='_reference_models')

    state = fields.Selection(
        selection=[('draft', 'Waiting'),
                   ('done', 'Accepted'),
                   ('cancel', 'Refused'),
                   ],
        required=True,
        default='draft',
    )

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    _type_to_field = {
        'char': 'char',
        'date': 'date',
        'datetime': 'datetime',
        'float': 'float',
        'integer': 'integer',
        'text': 'text',
        'boolean': 'boolean',
        'many2one': 'reference',
        'selection': 'char',
    }

    @api.model
    def create(self, vals):
        vals = vals.copy()
        field = self.env['ir.model.fields'].browse(vals.get('field_id'))
        if 'current_value' in vals:
            current_value = vals.pop('current_value')
            if field:
                current_field_name = self.get_field_for_type(field, 'current')
                vals[current_field_name] = current_value
        if 'new_value' in vals:
            new_value = vals.pop('new_value')
            if field:
                new_field_name = self.get_field_for_type(field, 'new')
                vals[new_field_name] = new_value
        return super(ResPartnerRevisionChange, self).create(vals)

    @api.model
    def get_field_for_type(self, field, current_or_new):
        assert current_or_new in ('new', 'current')
        field_type = self._type_to_field.get(field.ttype)
        if not field_type:
            # TODO: prevent to create unsupported types from the views
            raise NotImplementedError(
                'field type %s is not supported' % field_type
            )
        return '%s_value_%s' % (current_or_new, field_type)

    @api.multi
    def get_current_value(self):
        self.ensure_one()
        field_name = self.get_field_for_type(self.field_id, 'current')
        return self[field_name]

    @api.multi
    def get_new_value(self):
        self.ensure_one()
        field_name = self.get_field_for_type(self.field_id, 'new')
        return self[field_name]

    @api.multi
    def _convert_value_for_write(self, value):
        model = self.env[self.field_id.model_id.model]
        model_field_def = model._fields[self.field_id.name]
        return model_field_def.convert_to_write(value)

    @api.multi
    def apply(self):
        for change in self:
            if change.state in ('cancel', 'done'):
                continue
            partner = change.revision_id.partner_id
            value_for_write = change._convert_value_for_write(
                change.get_new_value()
            )
            partner.write({change.field_id.name: value_for_write})
