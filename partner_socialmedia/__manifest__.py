# -*- coding: utf-8 -*-
# Copyright 2018 Humanitarian Logistics Organisation e.V. - Stefan Becker
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Socialmedia',
    'summary': 'Add social media fields to contacts',
    'version': '10.0.1.0.0',
    'author': "humanilog, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/partner-contact",
    'category': 'CRM',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
}
