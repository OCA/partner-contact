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

from openerp import models, fields


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
    date = fields.Datetime()
    note = fields.Text()


class ResPartnerRevisionChange(models.Model):
    _name = 'res.partner.revision.change'
    _description = 'Partner Revision Change'
    _rec_name = 'new_value'

    revision_id = fields.Many2one(comodel_name='res.partner.revision',
                                  required=True,
                                  string='Revision',
                                  ondelete='cascade')
    field_id = fields.Many2one(comodel_name='ir.model.fields',
                               string='Field',
                               required=True)
    # TODO: different types of fields
    current_value = fields.Char('Current')
    new_value = fields.Char('New')
    state = fields.Selection(
        selection=[('draft', 'Waiting'),
                   ('done', 'Accepted'),
                   ('cancel', 'Refused'),
                   ],
        required=True,
        default='draft',
    )
