# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi
#    Copyright 2014 Camptocamp SA
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


class res_partner(orm.Model):
    """Add third field in address"""

    _inherit = "res.partner"
    _columns = {
        'street3': fields.char('Street 3'),
    }

    def _address_fields(self, cr, uid, context=None):
        fields = super(res_partner, self
                       )._address_fields(cr, uid, context=context)
        fields.append('street3')
        return fields


class res_country(orm.Model):
    """Override default adresses formatting of coutries"""

    _inherit = 'res.country'

    _defaults = {
        'address_format': ("%(street)s\n%(street2)s\n%(street3)s\n"
                           "%(city)s %(state_code)s %(zip)s\n"
                           "%(country_name)s"),
    }
