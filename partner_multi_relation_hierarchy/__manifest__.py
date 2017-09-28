# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner relation hierarchy",
    "version": "10.0.0.1.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "depends": [
        "partner_multi_relation",
    ],
    "data": [
        'views/res_partner.xml',
        'views/res_partner_relation_type.xml',
        'security/ir.model.access.csv',
    ],
    "auto_install": False,
    "installable": True,
}
