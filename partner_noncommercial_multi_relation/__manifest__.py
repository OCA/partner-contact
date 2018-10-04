# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV (https://therp.nl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Non Commercial Multi Relation',
    'version': '10.0.1.0.0',
    'author': 'Therp BV,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/partner-contact',
    'complexity': 'normal',
    'category': 'Customer Relationship Management',
    'license': 'AGPL-3',
    'depends': [
        'partner_noncommercial',
        'partner_multi_relation',
    ],
    'data': [
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}
