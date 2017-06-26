# -*- coding: utf-8 -*-
{
    'name': "Deduplicate Contacts (OCA)",
    'author': "Camptocamp,Sunflower IT,Odoo Community Association (OCA)",
    'category': 'Generic Modules/Base',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'mail',
        'base_manifest_extension',
    ],
    'depends_if_installed': [
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_partner_merge.xml',
    ],
    'installable': True,
    'post_load': 'post_load_hook',
}
