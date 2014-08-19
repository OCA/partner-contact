# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from openerp.osv import orm, fields


class ResCompany(orm.Model):

    _inherit = 'res.company'

    def on_change_city(self, cr, uid, ids, zip_id, context=None):
        result = {}
        if context is None:
            context = {}
        if zip_id:
            bzip = self.pool['res.better.zip'].browse(
                cr, uid, zip_id, context=context
            )
            country_id = bzip.country_id.id if bzip.country_id else False
            result = {
                'value': {
                    'zip': bzip.name,
                    'country_id': country_id,
                    'city': bzip.city,
                    'state_id': bzip.state_id.id if bzip.state_id else False
                }
            }
        return result

    _columns = {
        'better_zip_id': fields.many2one(
            'res.better.zip',
            'Location',
            select=1,
            help=('Use the city name or the zip code to search the location'),
        ),
    }
