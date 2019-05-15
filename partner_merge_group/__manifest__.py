# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Merge any partners",
    "summary": "Only partners in merge group can merge other partner",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.camptocamp.com",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/partner_merge_views.xml",
    ]
}
