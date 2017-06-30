# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Default sales discount per partner',
    'version': '8.0.1.0.0',
    'category': 'Partner Management',
    'license': 'AGPL-3',
    'author': 'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'depends': [
        'sale',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
