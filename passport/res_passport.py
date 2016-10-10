# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013-2014 Savoir-faire Linux
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

from openerp import fields


class res_passport(models.Model):
    _description = 'Passport'
    _name = 'res.passport'
    _columns = {
        'name': fields.char(
            'Owner name', help='Owner name (As printed into the passport).'),
        'number': fields.char(
            'Passport No', size=50, help='Passport number.'),
        'country_id': fields.many2one(
            'res.country', 'Delivery country', help="Country of deliverance."),
        'expiration_date': fields.date(
            'Expiration date', help="Expiration date of passport."),
        'birth_date': fields.date('Birth Date',
                                  help="Date of birth on passport."),
        'gender': fields.selection(
            [('male', 'Male'),
             ('female', 'Female')],
            'Gender', help="Gender."),
        'partner_id': fields.many2one('res.partner', 'Contact'),
    }

    def name_get(self, cr, uid, ids, context=None):
        if type(ids) in (int, long):
            ids = [ids]
        res = []
        for res_passport in self.browse(cr, uid, ids, context=context):
            name_elements = []
            if res_passport.country_id and res_passport.country_id.name:
                name_elements.append(res_passport.country_id.name)
            if res_passport.name:
                name_elements.append(res_passport.name)
            res.append((res_passport.id, ' | '.join(name_elements)))
        return res
