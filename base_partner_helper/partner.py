# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Sébastien BEAU <sebastien.beau@akretion.com>
#    Copyright 2014 Akretion
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


def split_char(char, output_number, size):
    words = char.split(' ')
    result = []
    word = words.pop(0)
    for index in range(0, output_number):
        result.append(word)
        word = ''
        while len(words) > 0:
            word = words.pop(0)
            if len(result[index] + ' %s' % word) > size:
                break
            else:
                result[index] += ' %s' % word
                word = ''
    return result


class ResPartner(orm.Model):
    _inherit = "res.partner"

    def _get_split_address(
            self, cr, uid, partner, output_number, max_size, context=None):
        """ This method allows to get a number of street fields according to
            your choice. Default is 2 large fields in Odoo (128 chars).
            In some countries you may use 3 or 4 shorter street fields.

            example:
            res = self.pool['res.partner']._get_split_address(
                cr, uid, picking.partner_id, 3, 35, context=context)
            address['street'], address['street2'], address['street3'] = res
        """
        street = partner.street or ''
        street2 = partner.street2 or ''
        if len(street) <= max_size and len(street2) <= max_size:
            result = ['' for i in range(0, output_number)]
            result[0] = street
            result[1] = street2
            return result
        elif street <= max_size:
            return [street] + split_char(street2, output_number - 1, max_size)
        else:
            return split_char(
                '%s %s' % (street, street2), output_number, max_size)
