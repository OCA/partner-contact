# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013-2014 Therp BV (<http://therp.nl>).
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
    "name": "Split street name and number",
    "version": "0.1",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "category": 'Tools',
    "description": """
This module introduces separate fields for street name and street number.

Changes to the OpenERP datamodel
================================

- Introduce two new fields for street name and number
- Keep 'Street' field as a function field to return street name + number
- Data written to the 'Street' field will be parsed into street name and number
  if possible. This will be performed upon installation of the module for
  existing partners.

Compatibility
=============
This module is compatible with OpenERP 7.0.
""",
    "depends": [
        'base'
        ],
    "data": [
        'view/res_partner.xml',
        ],
    'installable': True,
}
