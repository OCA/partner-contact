# Copyright 2015-2018 Therp BV (https://therp.nl).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Street name and number',
    'summary': 'Introduces separate fields for street name and street number.',
    'version': '11.0.1.0.0',
    'author': 'Therp BV,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/partner-contact',
    'category': 'Tools',
    'depends': [
        'base',
        'web',
        ],
    'data': [
        'views/res_partner.xml',
        'views/assets.xml',
        ],
    'installable': True,
    'license': 'AGPL-3',
    'post_init_hook': 'post_init_hook',
}
