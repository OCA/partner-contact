# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
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
from openerp import tools


class ResCompany(orm.Model):
    _inherit = 'res.company'

    def _get_logo_secondary(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.logo_secondary)
        return result

    def _set_logo_secondary(self, cr, uid, id, name, value, args, context=None):
        return self.write(
            cr, uid, [id],
            {'image': tools.image_resize_image_big(value)},
            context=context
        )

    def _has_logo_secondary(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.logo_secondary != False
        return result

    _columns = {
        'name_secondary': fields.char('Secondary name', size=128),
        'logo_secondary': fields.binary("Logo Secondary"),
        'image_medium': fields.function(
            _get_logo_secondary,
            fnct_inv=_set_logo_secondary,
            string="Medium-sized logo secondary",
            type="binary",
            multi="_get_logo_secondary",
            store={
                _inherit: (
                    lambda self, cr, uid, ids, c={}:
                    ids, ['logo_secondary'], 10
                ),
            }
        ),
        'image_small': fields.function(
            _get_logo_secondary,
            fnct_inv=_set_logo_secondary,
            string="Small-sized logo secondary",
            type="binary",
            multi="_get_logo_secondary",
            store={
                _inherit: (
                    lambda self, cr, uid, ids, c={}:
                    ids, ['image'], 10),
            },
        ),
        'has_logo_secondary': fields.function(
            _has_logo_secondary, type="boolean"
        ),

    }
