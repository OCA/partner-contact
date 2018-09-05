# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Relation Hierarchy",
    "version": "10.0.0.1.0",
    "website": "https://github.com/oca/partner-contact",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "depends": [
        "partner_multi_relation",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_relation_type.xml',
    ],
    "auto_install": False,
    "installable": True,
}
