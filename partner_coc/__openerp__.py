# -*- coding: utf-8 -*-
# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Partner CoC',
    'summary': "Adds a field 'Chamber Of Commerce Registration Number' to "
               "partner",
    'version': '8.0.1.0.0',
    'category': 'Web',
    'author': 'Onestein,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/partner-contact',
    'license': 'AGPL-3',
    'depends': [
        'partner_identification',
    ],
    'data': [
        'data/res_partner_id_category_data.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
