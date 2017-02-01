# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Alias",
    "summary": "Adds aliases to partner names.",
    "version": "10.0.1.0.0",
    "category": "Contacts",
    "website": "https://laslabs.com",
    "author": "Laslabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "partner_contact_personal_information_page",
        "partner_firstname",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/res_partner_alias_view.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
        "demo/res_partner_alias_demo.xml",
    ],
}
