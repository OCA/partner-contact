# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Sector",
    "summary": "Add partner sectors",
    "version": "9.0.2.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base_setup",
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
