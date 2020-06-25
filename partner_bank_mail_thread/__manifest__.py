# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Bank Mail Thread',
    'summary': """
        Enable a chatter on the partner bank accounts which will track
        updates done on a partner bank account""",
    'version': '10.0.2.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'views/res_partner_bank.xml',
    ],
}
