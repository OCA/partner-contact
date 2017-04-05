# -*- coding: utf-8 -*-
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
#    Author: Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


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


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_split_address(self, output_number, max_size):
        """ This method allows to get a number of street fields according to
            your choice. Default is 2 large fields in Odoo (128 chars).
            In some countries you may use 3 or 4 shorter street fields.

            example:
            res = self.env['res.partner']._get_split_address( 3, 35)
            street1, street2, street3 = res
        """
        self.ensure_one()
        street = self.street or ''
        street2 = self.street2 or ''
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
