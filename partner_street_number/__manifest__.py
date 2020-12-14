# Copyright 2013-2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Street name and number',
    'summary': 'Adds housenumber and doornumber also to contacts in partner form.',
    'version': '12.0.1.0.0',
    "license": "AGPL-3",
    'author': 'Therp BV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'category': 'Partner Management',
    'depends': ['web'],
    'data': [
        'views/res_partner.xml',
        ],
    'installable': True,
    'license': 'AGPL-3',
}
