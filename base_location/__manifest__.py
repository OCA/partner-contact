# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Location management (aka Better ZIP)',
    'version': '11.0.1.0.0',
    'depends': [
        'base_address_city'
    ],
    'author': "Camptocamp,"
              "ACYSOS S.L.,"
              "Alejandro Santana,"
              "Tecnativa,"
              "Odoo Community Association (OCA)",
    'license': "AGPL-3",
    'summary': '''Enhanced zip/npa management system''',
    'website': 'http://www.camptocamp.com',
    'data': ['views/better_zip_view.xml',
             'views/state_view.xml',
             'views/res_country_view.xml',
             'views/company_view.xml',
             'views/partner_view.xml',
             'security/ir.model.access.csv'],
    'demo': [
        'demo/better_zip.xml',
    ],
    'installable': True,
    'auto_install': False,
}
