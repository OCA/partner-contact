# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Contact Mapping in relations",
    "version": "10.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Customer Relationship Management",
    "summary": "Show partner addresses also as relations",
    "depends": [
        'partner_multi_relation',
    ],
    "data": [
        'data/data.xml',
        'views/res_partner_relation_type.xml',
    ],
    "installable": True,
}
