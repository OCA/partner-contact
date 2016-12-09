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
        for company in self:
            if company.better_zip_id:
                bz = company.better_zip_id
                company.zip = bz.name
                company.city = bz.city
                company.state_id = bz.state_id
                company.country_id = bz.country_id

    better_zip_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        select=1,
        help='Use the city name or the zip code to search the location',
    )
