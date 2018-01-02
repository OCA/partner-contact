# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Contacts in several partners",
    "summary": "Allow to have one contact in several partners",
    "version": "11.0.1.0.1",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Nicolas JEUDY,Odoo Community Association (OCA),Odoo SA",
    "license": "AGPL-3",
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
