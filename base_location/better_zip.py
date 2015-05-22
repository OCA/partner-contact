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


class BetterZip(orm.Model):
    " City/locations completion object"

    _name = "res.better.zip"
    _description = __doc__
    _order = "priority"

    _columns = {'priority': fields.integer('Priority', deprecated=True),
                'name': fields.char('ZIP'),
                'city': fields.char('City', required=True),
                'state_id': fields.many2one('res.country.state', 'State'),
                'country_id': fields.many2one('res.country', 'Country'),
                'code': fields.char('City Code', size=64,
                                    help="The official code for the city"),
                }

    _defaults = {'priority': 100}

    _sql_constraints = [(
        'location_uniq',
        'unique(name, city, state_id, country_id)',
        'This location already exists !')]

    def name_get(self, cursor, uid, ids, context=None):
        res = []
        for bzip in self.browse(cursor, uid, ids, context=context):
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

    def onchange_state_id(self, cr, uid, ids, state_id=False, context=None):
        result = {}
        if state_id:
            state = self.pool['res.country.state'].browse(
                cr, uid, state_id, context=context
            )
            if state:
                result['value'] = {'country_id': state.country_id.id}
        return result

    def name_search(
            self, cr, uid, name, args=None, operator='ilike', context=None,
            limit=100):
        if args is None:
            args = []
        if context is None:
            context = {}
        ids = []
        if name:
            ids = self.search(
                cr, uid, [('name', 'ilike', name)] + args, limit=limit)
        if not ids:
            ids = self.search(
                cr, uid, [('city', operator, name)] + args, limit=limit)
        return self.name_get(cr, uid, ids, context=context)
