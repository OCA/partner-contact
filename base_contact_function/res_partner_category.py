# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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


class res_partner_category(orm.Model):
    """
    Inherits partner_category
    """
    _inherit = 'res.partner.category'
    _columns = {
        'category_function_ids': fields.one2many(
            'res.partner.category.function',
            'category_id',
            'Functions'
        ),
    }

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            name = name.split(' / ')[-1]
            ids = self.search(cr, user, [('name', operator, name)] + args,
                              limit=limit, context=context)
            if ids:
                child_ids = self.search(
                    cr, user, [('parent_id', 'child_of', ids)],
                    limit=limit, context=context)
                if child_ids:
                    ids.extend(child_ids)
            # Remove duplicates and respect limit
            ids = list(set(ids))[:limit]
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)
