# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Email Format Checker',
    'version': '11.0.1.0.1',
    'summary': 'Validate email address field',
    'author': "Komit, Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/partner-contact',
    'category': 'Tools',
    'depends': ['base'],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': ['validate_email']
    },
}
