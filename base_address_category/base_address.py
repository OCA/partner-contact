# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Camptocamp SA (http://www.camptocamp.com) 
# All Right Reserved
#
# Author : Nicolas Bessi (Camptocamp), Joel Grand-Guillaume
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


from osv import osv, fields
import time
from mx import DateTime
import netsvc
import string

class ResPartnerAdressCategory(osv.osv):
    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name','parent_id'], context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = self.name_get(cr, uid, ids)
        return dict(res)
    def _check_recursion(self, cr, uid, ids):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from res_partner_address_category\
             where id in ('+','.join(map(unicode,ids))+')')
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True
        
    

    _description='Partner address Categories'
    _name = 'res.partner.address.category'
    _columns = {
        'name': fields.char('Category Name', required=True, size=64),
        'parent_id': fields.many2one('res.partner.address.category', 'Parent Category', select=True),
        'complete_name': fields.function(_name_get_fnc, method=True, type="char", string='Name'),
        'child_ids': fields.one2many('res.partner.address.category', 'parent_id', 'Childs Category'),
        'active' : fields.boolean('Active'),
    }
    _constraints = [
        (_check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active' : lambda *a: 1,
    }
    _order = 'parent_id,name'
    
ResPartnerAdressCategory()


class ResPartnerAddress(osv.osv):
    _inherit = "res.partner.address"
    
    _columns = {
        'category_id': fields.many2many('res.partner.address.category', 'res_partner_address_category_rel', 'adress_id', 'category_id', 'Adress categories'),
    }

ResPartnerAddress()