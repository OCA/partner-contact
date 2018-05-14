# -*- coding: utf-8 -*-
# Copyright 2016-2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Payment Return Risk',
    'version': '10.0.1.0.0',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'depends': [
        'partner_financial_risk',
        'account_payment_return',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
