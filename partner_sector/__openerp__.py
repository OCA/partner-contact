# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Sector",
    "summary": "Add partner sectors",
    "version": "9.0.1.0.1",
    "category": "Customer Relationship Management",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_sector_view.xml",
        "views/res_partner_view.xml",
    ]
}
