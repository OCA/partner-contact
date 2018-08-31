# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Show partner relations in own tab",
    "version": "7.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
This module adds the possibility to show certain partner relations in its own
tab instead of the list of all relations. This can be useful if certain
relation types are regularly used and should be overseeable at a glace.
    """,
    "category": "Customer Relationship Management",
    "depends": [
        'partner_relations',
        'web_compute_domain_x2many',
    ],
    "data": [
        "view/res_partner_relation_type.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
