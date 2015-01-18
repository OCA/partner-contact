# -*- coding: utf-8 -*-
#
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Contributor: Pedro Manuel Baeza <pedro.baeza@serviciosbaeza.com>
#                 Ignacio Ibeas <ignacio@acysos.com>
#                 Alejandro Santana <alejandrosantana@anubia.es>
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


class ResCompany(models.Model):

    _inherit = 'res.company'

    @api.multi
    @api.onchange('better_zip_id')
    def on_change_city(self):
        for record in self:
            if record.better_zip_id:
                record.zip = record.better_zip_id.name
                record.city = record.better_zip_id.city
                record.state_id = record.better_zip_id.state_id or False
                record.country_id = record.better_zip_id.country_id or False

    better_zip_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        select=1,
        help=('Use the city name or the zip code to search the location'),
    )
