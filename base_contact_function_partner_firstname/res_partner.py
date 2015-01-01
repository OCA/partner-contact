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
from openerp.osv import orm


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def create(self, cr, user, vals, context=None):
        context = self._basecontact_check_context(cr, user, 'create', context)
        if not vals.get('name') and vals.get('contact_id'):
            vals['name'] = self.browse(
                cr, user, vals['contact_id'], context=context).name
        if vals.get('end_date'):
            if vals.get('end_date', "Z") <= time.strftime('%Y-%m-%d'):
                vals['active'] = False
        if vals.get('contact_type') == 'standalone':
            contact_vals = dict(
                filter(lambda (k, v): k != 'parent_id', vals.iteritems())
            )
            contact_vals['active'] = True
            contact_vals['function_id'] = None
            vals['contact_id'] = super(res_partner, self).create(
                cr, user, contact_vals, context=context
            )
            self.write(cr, user, vals['contact_id'], {
                'firstname': vals.get('firstname', ''),
                'lastname': vals.get('lastname', ''),
            }, context=context)
        # Check if we create existing contact from company(ie: company is true)
        # Check if we create another function from contact view
        if vals.get('contact_type') == 'attached' or (
                not vals.get('contact_type') and vals.get('contact_id')):
            contact_info = self.browse(
                cr, user, vals.get('contact_id'), context=context)
            vals['firstname'] = contact_info.firstname
            vals['title'] = contact_info.title.id or ''

        res = super(res_partner, self).create(cr, user, vals, context=context)
        return res

    def write(self, cr, user, ids, vals, context=None):
        context = self._basecontact_check_context(cr, user, 'write', context)
        if vals.get('end_date'):
            if vals.get('end_date', "Z") <= time.strftime('%Y-%m-%d'):
                vals['active'] = False
        if vals.get('contact_type') == 'standalone':
            contact_vals = dict(
                filter(lambda (k, v): k != 'parent_id', vals.iteritems())
            )
            contact_vals['active'] = True
            contact_vals['function_id'] = None
            vals['contact_id'] = super(res_partner, self).write(
                cr, user, contact_vals, context=context
            )
        return super(res_partner, self).write(
            cr, user, ids, vals, context=context
        )
