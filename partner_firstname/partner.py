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
from openerp.osv.orm import Model, fields


class ResPartner(Model):
    """Adds lastname and firstname, name become a stored function field"""

    _inherit = 'res.partner'

    def init(self, cursor):
        cursor.execute('SELECT id FROM res_partner WHERE lastname IS NOT NULL Limit 1')
        if not cursor.fetchone():
            cursor.execute('UPDATE res_partner set lastname = name WHERE name IS NOT NULL')

    def _compute_name_custom(self, cursor, uid, ids, fname, arg, context=None):
        res = {}
        for rec in self.read(cursor, uid, ids, ['firstname', 'lastname']):
            names = [rec['lastname'],
                     rec['firstname']]
            fullname = " ".join([s for s in names if s])
            res[rec['id']] = fullname
        return res

    def _write_name(self, cursor, uid, partner_id, field_name, field_value, arg, context=None):
        return self.write(cursor, uid, partner_id, {'lastname': field_value})

    def create(self, cursor, uid, vals, context=None):
        """To support data backward compatibility we have to keep this overwrite even if we
        use fnct_inv: otherwise we can't create entry because lastname is mandatory and module
        will not install if there is demo data"""
        to_use = vals
        if vals.get('name'):
            corr_vals = vals.copy()
            corr_vals['lastname'] = corr_vals['name']
            del(corr_vals['name'])
            to_use = corr_vals
        return super(ResPartner, self).create(cursor, uid, to_use, context=context)

    _columns = {'name': fields.function(_compute_name_custom, string="Name",
                                        type="char", store=True,
                                        select=True, readonly=True,
                                        fnct_inv=_write_name),

                'firstname': fields.char("Firstname"),
                'lastname': fields.char("Lastname", required=True)}
