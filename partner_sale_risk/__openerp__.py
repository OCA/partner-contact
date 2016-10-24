# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Sale Risk',
    'summary': 'Manage partner risk in sales orders',
    'version': '9.0.1.0.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'author': 'Tecnativa, Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'depends': ['sale', 'partner_financial_risk'],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
}
