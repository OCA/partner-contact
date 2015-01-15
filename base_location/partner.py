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


class ResPartner(models.Model):
    _inherit = "res.partner"
    zip_id = fields.Many2one('res.better.zip', 'City/Location')

    @api.onchange('zip_id')
    def onchange_zip_id(self):
        if self.zip_id:
            self.zip = self.zip_id.zip
            self.city = self.zip_id.city
            self.country_id = self.zip_id.country_id
            self.state_id = self.zip_id.state_id
