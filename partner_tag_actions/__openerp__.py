# -*- coding: utf-8 -*-
# Copyright 2016 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Tag Actions',
    'version': '8.0.1.0.0',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'maintainer': 'Odoo Community Association (OCA)',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'General',
    'summary': 'Partner Tag Actions',
    'depends': [
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/res_groups_data.xml',
        'security/ir.model.access.csv',
        'views/partner_action_type_view.xml',
        'views/partner_action_view.xml',
        'views/partner_view.xml',
        'data/partner_action_data.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
