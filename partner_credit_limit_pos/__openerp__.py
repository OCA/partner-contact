# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name': 'Partner Credit Limit POS',
    'version': '0.1.0',
    'author': 'Versada',
    'category': 'Point of Sale',
    'website': 'http://versada.lt/',
    'licence': 'AGPL-3',
    'summary': 'Check partner credit limit in POS.',
    'depends': [
        'point_of_sale',
        'partner_credit_limit',
    ],
    'data': ['views/templates.xml'],
    'installable': True,
    'application': False,
}
