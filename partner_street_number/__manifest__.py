# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2013-2015 Therp BV (<http://therp.nl>).
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
    'name': 'Street name and number',
    'summary': 'Introduces separate fields for street name and street number.',
    'version': '10.0.1.0.0',
    'author': 'Therp BV,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/partner-contact',
    'category': 'Tools',
    'depends': [
        'base',
        'web',
        ],
    'data': [
        'views/res_partner.xml',
        'views/assets.xml',
        ],
    'installable': True,
    'license': 'AGPL-3',
    'post_init_hook': 'post_init_hook',
}
