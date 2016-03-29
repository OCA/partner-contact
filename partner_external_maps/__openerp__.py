# -*- coding: utf-8 -*-
# © 2015 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Partner External Maps',
    'version': '9.0.1.0.0',
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
