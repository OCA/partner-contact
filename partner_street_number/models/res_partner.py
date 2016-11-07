# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2013-2015 Therp BV (<http://therp.nl>).
#
#    @authors: Stefan Rijnhart, Ronald Portier
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
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('street_name', 'street_number')
    def _get_street(self):
        for partner in self:
            partner.street = ' '.join(
                filter(None, [partner.street_name, partner.street_number]))

    def _write_street(self):
        """
        Simplistically try to parse in case a value should get written
        to the 'street' field (for instance at import time, which provides
        us with a way of easily restoring the data when this module is
        installed on a database that already contains addresses).
        """
        for partner in self:
            street_name = partner.street.strip() if partner.street else False
            street_number = False
            if street_name:
                match = re.search(r'(.+)\s+(\d.*)', street_name)
                if match and len(match.group(2)) < 6:
                    street_name = match.group(1)
                    street_number = match.group(2)
            partner.street_name = street_name
            partner.street_number = street_number

    @api.multi
    def _display_address(self, without_company=False):
        """
        Inject a context key to prevent the 'street' name to be
        deleted from the result of _address_fields when called from
        the super.
        """
        return super(ResPartner, self.with_context(display_address=True)).\
            _display_address(without_company=without_company)

    @api.model
    def _address_fields(self):
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
        res = super(ResPartner, self)._address_fields()
        if 'street' in res and not (
                self._context.get('display_address')):
            res.remove('street')
        return res + ['street_name', 'street_number']

    street_name = fields.Char('Street name')
    street_number = fields.Char('Street number')
    # Must be stored as per https://bugs.launchpad.net/bugs/1253200
    street = fields.Char(
        compute='_get_street', store=True, inverse='_write_street')
