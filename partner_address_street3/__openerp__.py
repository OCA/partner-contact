# -*- coding: utf-8 -*-
# Copyright 2014 Nicolas Bessi, Alexandre Fayolle, Camptocamp SA
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Street3 in addresses',
    'version': '9.0.1.1.0',
    'author': "Camptocamp,Sodexis,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp',
    'category': 'Sales',
    'complexity': 'easy',
    'depends': ['base'],
    'website': 'http://www.camptocamp.com',
    'data': ['view/partner_view.xml'],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
