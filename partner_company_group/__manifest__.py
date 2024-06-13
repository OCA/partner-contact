# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Company Group',
    'summary': 'Adds the possibility to add a company group to a company',
    'version': '12.0.1.2.1',
    'category': 'Sales',
    'author': 'Camptocamp, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'crm',
        'sale',
    ],
    'website': 'https://github.com/OCA/partner-contact',
    'data': [
        'views/opportunity_view.xml',
        'views/contact_view.xml',
        'views/sale_order_view.xml',
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
