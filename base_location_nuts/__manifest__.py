# Copyright 2015 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'NUTS Regions',
    'category': 'Localisation/Europe',
    'version': '12.0.1.0.0',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/res_country_view.xml',
        'views/res_partner_nuts_view.xml',
        'views/res_partner_view.xml',
        'wizard/nuts_import_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': [
        'images/new_fields.png',
    ],
    'author': 'Tecnativa, '
              'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact/',
    'license': 'AGPL-3',
    'installable': True,
}
