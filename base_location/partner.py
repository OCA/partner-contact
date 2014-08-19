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


class ResPartner(orm.Model):
    _inherit = "res.partner"
    _columns = {
        'zip_id': fields.many2one('res.better.zip', 'City/Location'),
    }

    def onchange_zip_id(self, cursor, uid, ids, zip_id, context=None):
        if not zip_id:
            return {}
        if isinstance(zip_id, list):
            zip_id = zip_id[0]
        bzip_pool = self.pool['res.better.zip']
        bzip = bzip_pool.browse(cursor, uid, zip_id, context=context)
        return {
            'value': {
                'zip': bzip.name,
                'city': bzip.city,
                'country_id': bzip.country_id.id if bzip.country_id else False,
                'state_id': bzip.state_id.id if bzip.state_id else False,
            }
        }
