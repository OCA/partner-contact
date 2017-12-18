# -*- coding: utf-8 -*-
# Copyright 2017 Komit <http://komit-consulting.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Email Format Checker',
    'version': '10.0.1.0.0',
    'summary': 'Validate email address field',
    'author': "Komit, Odoo Community Association (OCA)",
    'website': 'http://komit-consulting.com',
    'category': 'Tools',
    'depends': ['base'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': ['validate_email']
    },
}
