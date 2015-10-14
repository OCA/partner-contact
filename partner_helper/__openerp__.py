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

{
    'name': 'Partner Helper',
    'version': '8.0.0.1.0',
    'author': "Akretion,Odoo Community Association (OCA)",
    'maintainer': 'Akretion',
    'category': 'Warehouse',
    'depends': [
        'base',
    ],
    'description': """
Partner Helper
==============
The purpose of this module is to gather generic partner methods.
It avoids to grow up excessively the number of modules in Odoo
for small features.

Description
-----------
Add specific helper methods to deal with partners:

* _get_split_address():
    This method allows to get a number of street fields according to
    your choice. 2 fields by default in Odoo with 128 width chars.
    In some countries you have constraints on width of street fields and you
    should use 3 or 4 shorter fields.
    You also need of this feature to avoid headache with overflow printing task

* other_method():

Contributors
------------
* Sébastien BEAU <sebastien.beau@akretion.com>
* David BEAL <david.beal@akretion.com>


    """,
    'website': 'http://www.akretion.com/',
    'data': [],
    'tests': [],
    'installable': False,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
