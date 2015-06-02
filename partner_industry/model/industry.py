# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Jacques-Etienne Baudoux <je@bcim.be>
#    Copyright 2015 BCIM sprl
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


class Industry(orm.Model):
    _name = 'res.partner.category.industry'
    _inherit = 'res.partner.category'

    _columns = {
        'code': fields.char('Code', size=16),
        'parent_id': fields.many2one(_name, 'Parent Category', select=True, ondelete='cascade'),
        'partner_ids': fields.many2many(
            'res.partner',
            'res_partner_industry_rel', 'industry_id', 'partner_id',
            'Partners'),
    }
