# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Vaucher
#    Copyright 2012 Camptocamp SA
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


class ResPartner(orm.Model):
    """
    Add relation affiliate_ids
    """
    _name = "res.partner"
    _inherit = "res.partner"

    _columns = {
        'child_ids': fields.one2many(
            'res.partner', 'parent_id',
            'Contacts', domain=[('is_company', '=', False)]),
        'affiliate_ids': fields.one2many(
            'res.partner', 'parent_id',
            'Affiliates', domain=[('is_company', '=', True)]),
    }
