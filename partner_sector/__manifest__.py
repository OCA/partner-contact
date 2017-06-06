# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016-2017 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Sector",
    "summary": "Add partner sectors",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_sector_view.xml",
        "views/res_partner_view.xml",
    ]
}
