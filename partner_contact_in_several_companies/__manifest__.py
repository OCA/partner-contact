# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Contacts in several partners",
    "summary": "Allow to have one contact in several partners",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://odoo-community.org/",
    "author": "Odoo Community Association (OCA),Odoo SA",
    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "base",
        "partner_contact_personal_information_page",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/ir_actions.xml",
    ],
}
