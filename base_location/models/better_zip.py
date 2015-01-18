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
from openerp import models, fields, api


class BetterZip(models.Model):
    '''City/locations completion object'''

    _name = "res.better.zip"
    _description = __doc__
    _order = "name asc"

    name = fields.Char('ZIP')
    code = fields.Char('City Code', size=64,
                       help="The official code for the city")
    city = fields.Char('City', required=True)
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')

    @api.multi
    def name_get(self):
        res = []
        for bzip in self:
            if bzip.name:
                name = [bzip.name, bzip.city]
            else:
                name = [bzip.city]
            if bzip.state_id:
                name.append(bzip.state_id.name)
            if bzip.country_id:
                name.append(bzip.country_id.name)
            res.append((bzip.id, ", ".join(name)))
        return res

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('name', 'ilike', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('city', operator, name)] + args, limit=limit)
        return recs.name_get()
