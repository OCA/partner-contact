# -*- coding: utf-8 -*-
# © 2014-2016 Camptocamp SA (Author: Romain Deheele)
# © 2017 senseFly, Amaris (Author: Quentin Theuret)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Continent management',
    'version': '10.0.1.1.0',
    'depends': [
        'base',
        'sales_team',
    ],
    'author': "Camptocamp,senseFly,Amaris,Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'category': 'Generic Modules/Base',
    'data': [
        'views/continent.xml',
        'views/country.xml',
        'views/partner.xml',
        'data/continent_data.xml',
        'data/country_data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
