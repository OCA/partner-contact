# -*- coding: utf-8 -*-
# © 2016 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Partner Payment Return Risk',
    'version': '9.0.1.0.0',
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
