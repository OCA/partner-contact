# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
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
    'name': 'Partner first name, last name',
    'description': """
This module splits first name and last name for non company partners
====================================================================

The field 'name' becomes a stored function field concatenating lastname and
firstname
Note: in version 7.0, installing this module invalidates a yaml test in the
'edi' module

Contributors
============
Jonathan Nemry <jonathan.nemry@acsone.eu>
Olivier Laurent <olivier.laurent@acsone.eu>

""",
    'version': '1.2',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp, Acsone',
    'category': 'Extra Tools',
    'website': 'http://www.camptocamp.com, http://www.acsone.eu',
    'depends': ['base'],
    'data': [
        'partner_view.xml',
        'res_user_view.xml',
    ],
    'demo': [],
    'test': [],
    'auto_install': False,
    'installable': True,
    'images': []
}
