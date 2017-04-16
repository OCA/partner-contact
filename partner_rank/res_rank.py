##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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


class res_rank(orm.Model):
    _description = 'Rank'
    _name = 'res.rank'

    _columns = {
        'name': fields.char(
            'Name', help='Rank name.'),
        'description': fields.text(
            'Description', help='Rank description.'),
        'priority': fields.integer(
            'Priority', help='Rank priority (the lower the most important).'),
        'partner_ids': fields.one2many(
            'res.partner', 'rank_id', 'Partner'),
    }

    _sql_constraints = [
        ('priority_uniq', 'UNIQUE(priority)', 'The priority must be unique!'),
    ]

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if type(ids) in (int, long):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context):
            res.append((record.id, str(record.priority) +
                       ' - ' + record.name))
        return res
