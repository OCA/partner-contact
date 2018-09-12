# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016-2017 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Sector",
    "summary": "Add partner sectors",
    "version": "10.0.1.2.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/partner_sector_security.xml",
        "views/res_partner_sector_view.xml",
        "views/res_partner_view.xml",
        "views/base_config_settings.xml",
        "views/sale_config_settings.xml"
    ]
}
