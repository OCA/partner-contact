# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# Copyright 2017 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Deduplicate Contacts (No CRM)",
    'summary': "Partner merge wizard without dependency on CRM",
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'category': 'Generic Modules/Base',
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'views/base_partner_merge.xml',
    ],
    'installable': True,
}
