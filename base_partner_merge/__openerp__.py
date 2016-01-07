# -*- coding: utf-8 -*-
{
    'name': 'Base Partner Merge',
    'author': "OpenERP S.A.,Odoo Community Association (OCA)",
    'category': 'Generic Modules/Base',
    'version': '8.0.0.1.0',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'base_partner_merge_view.xml',
    ],
    'installable': True,
}
