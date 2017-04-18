# -*- coding: utf-8 -*-
{
    'name': "Deduplicate Contacts (No CRM)",
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'category': 'Generic Modules/Base',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_partner_merge.xml',
    ],
    'installable': True,
}
