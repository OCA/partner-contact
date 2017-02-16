# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Contact Configuration',
    'summary': """
        Adds menu configuration access through the 'contacts' module main menu
        """,
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://acsone.eu',
    'depends': ['base',
                'contacts'
                ],
    'data': ['views/partner_contact.xml'
             ],
    'demo': [
    ],
}
