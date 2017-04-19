# -*- coding: utf-8 -*-
# Copyright 2016 Acsone S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Partner Gln',
    'summary': """
        Adds a field GLN on partners to manage GLN (EAN) code.""",
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Acsone S.A.,Odoo Community Association (OCA)',
    'contributors': [
        'Denis Roussel <denis.roussel@acsone.eu>',
    ],
    'website': 'https://www.acsone.eu',
    'depends': ['base'
                ],
    'python': ['stdnum'
               ],
    'data': ['views/partner_view.xml'
             ],
    'demo': [
    ],
}
