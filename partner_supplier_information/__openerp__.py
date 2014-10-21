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

{
    'name': 'Partner Supplier Information',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'category': 'Customer Relationship Management',
    'description': """
Partner Supplier Informations
=============================

This module adds some fields for supplier:

* Legal form
* NGO: If partner is a Non-governmental organization (NGO)
* Confirmed supplier
* Registration number
* Registration date
* Registration location
* Matriculation Number


Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
""",
    'depends': [
        'account',
    ],
    'data': [
        'res_partner_view.xml',
    ],
    'installable': True,
}
