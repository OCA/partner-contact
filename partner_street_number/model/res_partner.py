# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013-2014 Therp BV (<http://therp.nl>).
#
#    @autors: Stefan Rijnhart, Ronald Portier
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

import re
from openerp.osv import orm, fields


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def get_street(self, cr, uid, partner, context=None):
        """
        Allow to override the field function's value composition

        :param partner: res.partner browse record
        :rtype: string
        """
        return ' '.join(filter(None, [
            partner.street_name,
            partner.street_number,
        ]))

    def _get_street(self, cr, uid, select, field_name, args, context=None):
        """ Delegates the function field 'street' to an inheritable method"""
        res = {}
        for partner in self.browse(cr, uid, select, context=context):
            res[partner.id] = self.get_street(
                cr, uid, partner, context=context)
        return res

    def _write_street(self, cr, uid, ids, name, value, arg, context=None):
        """
        Simplistically try to parse in case a value should get written
        to the 'street' field (for instance at import time, which provides
        us with a way of easily restoring the data when this module is
        installed on a database that already contains addresses).
        """
        street_name = value and value.strip() or False
        street_number = False
        if value:
            match = re.search('(.+)\s+(\d.*)', value.strip())
            if match and len(match.group(2)) < 6:
                street_name = match.group(1)
                street_number = match.group(2)
        return self.write(cr, uid, ids, {
            'street_name': street_name,
            'street_number': street_number,
            }, context=context)

    def _display_address(
            self, cr, uid, address, without_company=False, context=None):
        """
        Inject a context key to prevent the 'street' name to be
        deleted from the result of _address_fields when called from
        the super.
        """
        local_context = dict(context or {}, display_address=True)
        return super(ResPartner, self)._display_address(
            cr, uid, address, without_company=without_company,
            context=local_context)

    def _address_fields(self, cr, uid, context=None):
        """
        Pass on the fields for address synchronisation to contacts.

        This method is used on at least two occassions:

        [1] when address fields are synced to contacts, and
        [2] when addresses are formatted

        We want to prevent the 'street' field to be passed in the
        first case, as it has a fallback write method which should
        not be triggered in this case, while leaving the field in
        in the second case. Therefore, we remove the field
        name from the list of address fields unless we find the context
        key that this module injects when formatting an address.

        Could have checked for the occurrence of the synchronisation
        method instead, leaving the field in by default but that could
        lead to silent data corruption should the synchronisation API
        ever change.
        """
        res = super(ResPartner, self)._address_fields(cr, uid, context=context)
        if 'street' in res and not (
                context and context.get('display_address')):
            res.remove('street')
        return res + ['street_name', 'street_number']

    _columns = {
        'street_name': fields.char(
            'Street name', size=118),
        'street_number': fields.char(
            'Street number', size=10),
        'street': fields.function(
            _get_street, fnct_inv=_write_street,
            type='char', string="Street",
            # Must be stored as per https://bugs.launchpad.net/bugs/1253200
            store={
                'res.partner': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['street_name', 'street_number'], 10),
                },
            ),
        }
