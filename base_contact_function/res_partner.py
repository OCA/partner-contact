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

import time
from openerp.osv import orm, fields


class res_partner(orm.Model):
    """
    Inherits partner and adds function_ids : List of functions
    """
    _inherit = 'res.partner'

    def onchange_partner_function(self, cr, uid, ids, part, context=None):
        partner_pool = self.pool['res.partner']
        if not part:
            return {'value': None}
        partner_ids = partner_pool.search(cr, uid, [('id', '=', part)])
        function_ids = partner_pool.browse(
            cr, uid, partner_ids, context=context)[0].function_ids
        result = []
        if function_ids:
            for line in function_ids:
                result.append(line.id)
        dom = {'function_id': [('id', 'in', result)]}
        return {'domain': dom}

    def _get_history_lines(self, cr, uid, ids, name, arg, context=None):
        res = {}
        res_partner_pool = self.pool.get('res.partner')
        for record in self.browse(cr, uid, ids, context=context):

            if record.is_company:
                return res
            contact_ids = res_partner_pool.search(
                cr, uid, [
                    ('contact_id', '=', record.id),
                    ('active', '=', False),
                ], context=context
            )
            res[record.id] = [
                x.id for x in res_partner_pool.browse(cr, uid, contact_ids)
                if x.end_date and x.end_date <= time.strftime('%Y-%m-%d')
            ]
        return res

    _columns = {
        'function_ids': fields.many2many(
            'res.partner.function',
            'function_partner_rel',
            'partner_id',
            'function_id',
            'Functions',
        ),
        'start_date': fields.date('Start date'),
        'end_date': fields.date('End date'),
        'naming': fields.char(
            'Naming',
            help="Naming.",
        ),
        'function_id': fields.many2one(
            'res.partner.function',
            'Position Occupied',
        ),
        'other_contact_history_ids': fields.function(
            _get_history_lines,
            relation="res.partner",
            method=True,
            type="one2many",
        ),
        # Replace company by Organisation
        'use_parent_address': fields.boolean(
            'Use Organisation Address',
            help="Select this if you want to set organisation's address "
                 "information  for this contact",
        ),

    }
