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
from openerp.tools.translate import _


class ResPartner(orm.Model):
    """Adds lastname and firstname, name become a stored function field"""

    _inherit = 'res.partner'

    def init(self, cursor):
        cursor.execute(
            'SELECT id FROM res_partner WHERE lastname IS NOT NULL Limit 1'
        )
        if not cursor.fetchone():
            cursor.execute(
                'UPDATE res_partner set lastname = name WHERE name IS NOT NULL'
            )
            # Create Sql constraint if table is not empty
            cursor.execute('SELECT id FROM res_partner Limit 1')
            if cursor.fetchone():
                cursor.execute(
                    'ALTER TABLE res_partner '
                    'ALTER COLUMN lastname SET NOT NULL'
                )

    def _prepare_name_custom(self, cursor, uid, partner, context=None):
        """
        This function is designed to be inherited in a custom module
        """
        names = (partner.lastname, partner.firstname)
        fullname = " ".join([s for s in names if s])
        return fullname

    def _compute_name_custom(self, cursor, uid, ids, fname, arg, context=None):
        res = {}
        for partner in self.browse(cursor, uid, ids, context=context):
            res[partner.id] = self._prepare_name_custom(
                cursor, uid, partner, context=context)
        return res

    def _write_name(
            self, cursor, uid, partner_id, field_name, field_value, arg,
            context=None):
        """Try to reverse the effect of _compute_name_custom:
        * if the partner is not a company and the firstname does not
          change in the new name then firstname remains untouched and
          lastname is updated accordingly
        * otherwise lastname=new name and firstname=False
        In addition an heuristic avoids to keep a firstname without a
        non-blank lastname
        """
        field_value = (
            field_value if field_value and not field_value.isspace() else False
        )
        vals = {'lastname': field_value, 'firstname': False}
        if field_value:
            flds = self.read(
                cursor,
                uid,
                [partner_id],
                ['firstname', 'is_company'],
                context=context
            )[0]
            if not flds['is_company']:
                to_check = ' %s' % flds['firstname']
                if field_value.endswith(to_check):
                    ln = field_value[:-len(to_check)].strip()
                    if ln:
                        vals['lastname'] = ln
                        del(vals['firstname'])
                    else:
                        # If the lastname is deleted from the new name
                        # then the firstname becomes the lastname
                        vals['lastname'] = flds['firstname']

        return self.write(cursor, uid, partner_id, vals, context=context)

    def copy_data(self, cr, uid, _id, default=None, context=None):
        """Avoid to replicate the firstname into the name when
        duplicating a partner
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
        return super(ResPartner, self).copy_data(
            cr, uid, _id, default, context=context
        )

    def create(self, cursor, uid, vals, context=None):
        """To support data backward compatibility we have to keep this
        overwrite even if we use fnct_inv: otherwise we can't create
        entry because lastname is mandatory and module will not install
        if there is demo data
        """
        to_use = vals
        if 'name' in vals:
            corr_vals = vals.copy()
            corr_vals['lastname'] = corr_vals['name']
            del(corr_vals['name'])
            to_use = corr_vals
        return super(ResPartner, self).create(
            cursor, uid, to_use, context=context
        )

    _columns = {
        'name': fields.function(
            _compute_name_custom,
            string="Name",
            type="char",
            store=True,
            select=True,
            readonly=True,
            fnct_inv=_write_name
        ),

        'firstname': fields.char("Firstname"),
        'lastname': fields.char("Lastname", required=True),
    }
