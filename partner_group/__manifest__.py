# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Group',
    'summary': 'Group partners by groups (other partner)',
    'version': '11.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Contact',
    'website': 'https://github.com/OCA/partner-contact',
    'author': 'Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
}
