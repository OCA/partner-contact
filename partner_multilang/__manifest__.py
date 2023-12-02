# Copyright 2023 Rosen Vladimirov
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Multilang',
    'summary': """
        Multilang partner names.""",
    'version': '16.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Localization',
    'author': 'Rosen Vladimirov,Odoo Community Association (OCA)',
    "website": "https://github.com/OCA/partner-contact",
    'conflicts': [
        'base_search_fuzzy',
    ],
    'depends': [
        'base',
    ],
    'data': [
    ],
    'demo': [
    ],
    'installable': True,
    "pre_init_hook": "pre_init_hook",
}
