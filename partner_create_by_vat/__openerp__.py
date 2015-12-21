# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# See README.rst file on addons root folder for license details

{
    'name': 'Partner Create by VAT',
    'summary': 'Create Partners by VAT from VIES Webservice',
    'version': '8.0.1.0.0',
    'category': 'Customer Relationship Management',
    'author': 'Forest and Biomass Services Romania, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.forbiom.eu',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': ['stdnum', 'suds'],
    },
    'depends': ['base_vat'],
    'data': ['views/res_partner_view.xml'],
    'images': ['static/description/customer.png',
               'static/description/customer1.png',
               'static/description/customer2.png'],
    'auto_install': False,
}
