# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner External Maps',
    'version': '10.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Add Map and Map Routing buttons on partner form to '
               'open GMaps, OSM, Bing and others',
    'author': 'Akretion, '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml',
        'views/map_website_view.xml',
        'data/map_website_data.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
    ],
    'post_init_hook': 'set_default_map_settings',
    'installable': True,
}
