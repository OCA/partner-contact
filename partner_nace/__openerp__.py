# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "NACE Activities",
    "version": "8.0.1.0.0",
    "category": "Localisation/Europe",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [
            "requests",
        ],
    },
    "depends": [
        "base",
    ],
    "data": [
        'views/res_partner_nace_view.xml',
        'views/res_partner_view.xml',
        'wizard/nace_import_view.xml',
        'security/ir.model.access.csv',
    ]
}
