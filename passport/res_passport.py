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

from openerp.osv import fields, orm


class res_passport(orm.Model):
    _description = 'Passport'
    _name = 'res.passport'
    _columns = {
        'name': fields.char('Owner name', size=256, select=True,
                            help='Owner name (As printed into the passport).'),
        'number': fields.char('Passport No', size=50,
                              help='Passport number.'),
        'country_id': fields.many2one('res.country', 'Delivery country',
                                      help="Delivery country."),
        'expiration_date': fields.date('Expiration date',
                                       help="Expiration date."),
        'birth_date': fields.date('Birth Date', help="Birth Date."),
        'gender': fields.selection([('male', 'Male'),
                                    ('female', 'Female')],
                                   'Gender',
                                   help="Gender."),
    }

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        reads = self.read(cr, uid, ids, ['name', 'country_id'], context)

        for record in reads:
            name = record['name']
            if record['country_id']:
                name = record['country_id'][1] + ' | ' + name
            res.append((record['id'], name))
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
