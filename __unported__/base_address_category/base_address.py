# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010-2013 Camptocamp SA (http://www.camptocamp.com)
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp), Joel Grand-Guillaume
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
##############################################################################


from openerp.osv import fields, orm


class ResPartnerAdressCategory(orm.Model):

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = '%s / %s ' % (record['parent_id'][1], name)
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = self.name_get(cr, uid, ids)
        return dict(res)

    def _check_recursion(self, cr, uid, ids):
        level = 100
        while ids:
            cr.execute('select distinct parent_id '
                       'from res_partner_address_category '
                       'where id in %s', ids)
            ids = [parent_id for (parent_id,) in cr.fetchall() if parent_id]
            if not level:
                return False
            level -= 1
        return True

    _name = 'res.partner.address.category'
    _description = 'Partner address Categories'
    _columns = {
        'name': fields.char('Category Name', required=True, size=64),
        'parent_id': fields.many2one('res.partner.address.category',
                                     'Parent Category',
                                     select=True),
        'complete_name': fields.function(_name_get_fnc,
                                         type="char",
                                         string='Name'),
        'child_ids': fields.one2many('res.partner.address.category',
                                     'parent_id',
                                     'Children Category'),
        'active': fields.boolean('Active'),
    }
    _constraints = [
        (_check_recursion,
         'Error: you can not create recursive categories.',
         ['parent_id'])
    ]
    _defaults = {
        'active': lambda *a: 1,
    }
    _order = 'parent_id,name'


class ResPartnerAddress(orm.Model):
    _inherit = "res.partner.address"

    _columns = {
        'category_id': fields.many2many('res.partner.address.category',
                                        'res_partner_address_category_rel',
                                        'adress_id',
                                        'category_id',
                                        'Address categories'),
    }
