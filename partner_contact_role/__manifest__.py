# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Contact Role',
    'summary': """Add roles to partners.""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'depends': [
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_role.xml',
        'views/res_partner.xml',
    ],
}
