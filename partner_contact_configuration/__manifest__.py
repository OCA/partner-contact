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
    'maintainers': ['rousseldenis'],
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'base',
        'contacts'
    ],
    'data': [
        'views/partner_contact.xml'
    ],
}
