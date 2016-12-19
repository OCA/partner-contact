# -*- coding: utf-8 -*-
# Copyright 2016 Nicolas Bessi, Copyright Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Location management (aka Better ZIP)',
    'version': '9.0.1.0.0',
    'depends': ['base'],
    'author': "Camptocamp,"
              "ACYSOS S.L.,"
              "Alejandro Santana,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza,"
              "Odoo Community Association (OCA)",
    'license': "LGPL-3",
    'contributors': [
        'Nicolas Bessi <nicolas.bessi@camptocamp.com>',
        'Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>',
        'Ignacio Ibeas (Acysos S.L.)',
        'Alejandro Santana <alejandrosantana@anubia.es>',
        'Sandy Carter <sandy.carter@savoirfairelinux.com>',
        'Yannick Vaucher <yannick.vaucher@camptocamp.com>',
    ],
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
    'installable': False,
    'auto_install': False,
}
