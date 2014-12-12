# -*- coding: utf-8 -*-
#
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Contributor: Pedro Manuel Baeza <pedro.baeza@serviciosbaeza.com>
#                 Ignacio Ibeas <ignacio@acysos.com>
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


class BetterZip(models.Model):

    " City/locations completion object"

    _name = "res.better.zip"
    _description = __doc__

    priority = fields.Integer('Priority', deprecated=True)
    name = fields.Char('Name', compute='_get_name', store=True)
    zip = fields.Char('ZIP')
    city = fields.Char('City', required=True)
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    code = fields.Char(
        'City Code', size=64, help="The official code for the city")

    @api.one
    @api.depends(
        'zip',
        'city',
        'state_id',
        'state_id.name',
        'country_id',
        'country_id.name',
        )
    def _get_name(self):
        self.name = ('(%s) %s, %s, %s') % (
            self.zip or '',
            self.city or '',
            self.state_id and self.state_id.name or '',
            self.country_id and self.country_id.name or '',
            )

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id.id
