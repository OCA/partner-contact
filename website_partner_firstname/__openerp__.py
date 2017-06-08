# -*- coding: utf-8 -*-
# © <2015> <Paul Catinean>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Firstname / Lastname',
    'summary': "Suppliment for partner_firstname module implementing first "
               "name and last name in e-shop at checkout",
    'version': '8.0.1.0.0',
    'author': "Paul Catinean, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'maintainer': 'Paul Catinean',
    'category': 'Extra Tools',
    'depends': [
        'website_sale',
        'partner_firstname'
    ],
    'data': [
        'templates.xml',
    ],
    'auto_install': False,
    'installable': True,
}
