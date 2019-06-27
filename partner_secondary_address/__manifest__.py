# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner Secondary Address',
    'summary': 'Adds a secondary address to contacts.',
    'author': 'Robin Keunen, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'category': 'Customer Relationship Management',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
        ],
    'data': [
        'views/res_partner.xml',
    ],
}
