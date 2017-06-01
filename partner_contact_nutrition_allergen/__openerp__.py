# -*- coding: utf-8 -*-
# Copyright 2016 Ursa Information Systems <http://ursainfosystems.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner Contact Nutrition Allergens",
    "summary": "Set the nutrition allergens of your contacts",
    "version": "9.0.1.0.0",
    "category": "Health",
    "website": "http://ursainfosystems.com",
    "author": "Ursa Information Systems, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "partner_contact_nutrition",
        "stock",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
}
