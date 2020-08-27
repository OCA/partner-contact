# -*- coding: utf-8 -*-
{
    "name": "Contacts in several partners",
    "summary": "Allow to have one contact in several partners",
    "version": "13.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Fabio Oliveira, Odoo Community Association (OCA),Odoo SA",
    "license": "AGPL-3",
    "depends": [
        "base",
        "contacts",
        "partner_contact_personal_information_page",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/ir_actions.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
