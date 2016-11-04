# -*- coding: utf-8 -*-
# ©  2015 Forest and Biomass Services Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Automatic partner creation based on VAT number',
    'summary': 'Using VIES webservice, name and address information will '
               'be fetched and added to the partner.',
    'version': '10.0.1.0.0',
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
    'images': ['static/description/icon.png',
               'static/description/customer.png',
               'static/description/customer1.png'],
    'auto_install': False,
}
