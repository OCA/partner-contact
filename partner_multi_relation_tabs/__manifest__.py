# -*- coding: utf-8 -*-
# © 2014-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Show partner relations in own tab",
    "version": "10.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "depends": [
        'partner_multi_relation',
    ],
    "data": [
        "views/res_partner_relation_type.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
