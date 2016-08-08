# -*- coding: utf-8 -*-
# Copyright 2016 Acsone S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Identification Gln',
    'summary': """
        This addon extends "Partner Identification Numbers"
        to provide a number category for GLN registration""",
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Acsone S.A.,Odoo Community Association (OCA)',
    'website': 'https://www.acsone.eu',
    'external_dependencies': {
        'python': ['stdnum'
                   ],
    },
    'depends': ['partner_identification'
                ],
    'data': ['data/partner_identification_gln.xml'
             ],
    'installable': True,
}
