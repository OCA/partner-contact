# -*- coding: utf-8 -*-
# Copyright 2013-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner relations",
    "version": "10.0.1.0.2",
    "author": "Therp BV,Camptocamp,Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "website": "https://github.com/oca/partner-contact",
    "depends": [
        'sales_team',
    ],
    "demo": [
        "data/demo.xml",
    ],
    "data": [
        "views/res_partner_relation_all.xml",
        'views/res_partner.xml',
        'views/res_partner_relation_type.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    "auto_install": False,
    "installable": True,
}
