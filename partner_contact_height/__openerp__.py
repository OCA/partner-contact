# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner Contact Height",
    "summary": "Provide contact height.",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://ursainfosystems.com",
    "author": "Ursa Information Systems, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "partner_contact_personal_information_page",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
}
