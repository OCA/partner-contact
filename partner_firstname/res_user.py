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
from openerp.osv import orm
from openerp.tools.translate import _


class ResUsers(orm.Model):

    _inherit = 'res.users'

    def create(self, cr, user, vals, context=None):
        """To support data backward compatibility we have to keep this
        overwrite even if we use fnct_inv: otherwise we can't create
        entry because lastname is mandatory and module will not install
        if there is demo data

        This fixes the unittests in stock when partner_firstname is
        installed
        """
        vals2 = vals.copy()

        if 'name' in vals:
            vals2['lastname'] = vals2['name']
        elif 'lastname' not in vals and 'partner_id' in vals:
            res_partner = self.pool.get('res.partner')
            partner = res_partner.browse(cr, user, vals2['partner_id'],
                                         context)
            vals2['lastname'] = partner.lastname
        elif 'login' in vals and 'lastname' not in vals:
            vals2['lastname'] = vals2['login']
        return super(ResUsers, self).create(cr, user, vals2, context=context)

    def copy_data(self, cr, uid, _id, default=None, context=None):
        """Avoid to replicate the firstname into the name when
         duplicating a user
        """
        default = default or {}
        if not default.get('lastname'):
            default = default.copy()
            default['lastname'] = (
                _('%s (copy)') % self.read(
                    cr,
                    uid,
                    [_id],
                    ['lastname'],
                    context=context
                )[0]['lastname']
            )
            if default.get('name'):
                del(default['name'])
        return super(ResUsers, self).copy_data(
            cr, uid, _id, default, context=context
        )
