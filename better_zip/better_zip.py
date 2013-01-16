# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Nicolas Bessi. Copyright Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv.orm import Model, fields


class BetterZip(Model):
    " Zip/NPA object"

    _name = "res.better.zip"
    _description = __doc__
    _order = "priority"

    _columns = {'priority': fields.integer('Priority'),
                'name': fields.char('ZIP', required=True),
                'city': fields.char('City', required=True),
                'state_id': fields.many2one('res.country.state', 'State'),
                'country_id': fields.many2one('res.country', 'Country'),
                }

    _defaults = {'priority': 100}

    def name_get(self, cursor, uid, ids, context=None):
        res = []
        for bzip in self.browse(cursor, uid, ids):
            res.append((bzip.id, u"%s %s" % (bzip.name, bzip.city)))
        return res


class Partner(Model):
    _inherit = "res.partner"
    _columns = {'zip_id': fields.many2one('res.better.zip', 'ZIP/PN')}

    def onchange_zip_id(self, cursor, uid, ids, zip_id, context=None):
        if not zip_id:
            return {}
        if isinstance(zip_id, list):
            zip_id = zip_id[0]
        bzip = self.pool['res.better.zip'].browse(cursor, uid, zip_id, context=context)
        return {'value': {'zip': bzip.name, 'city': bzip.city,
                          'country_id': bzip.country_id.id, 'state_id': bzip.state_id.id}}
