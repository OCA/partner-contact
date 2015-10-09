# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner External Maps module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Partner External Maps',
    'version': '8.0.0.1.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Add Map and Map Routing buttons on partner form to '
               'open GMaps, OSM, Bing and others',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'partner_view.xml',
        'map_website_data.xml',
        'map_website_view.xml',
        'users_view.xml',
        'security/ir.model.access.csv',
    ],
    'post_init_hook': 'set_default_map_settings',
    'installable': True,
}
