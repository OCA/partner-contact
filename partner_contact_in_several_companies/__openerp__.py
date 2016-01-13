# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Contacts in several partners",
    "summary": "Allow to have one contact in several partners",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://odoo-community.org/",
    "author": "Odoo Community Association (OCA)",
    "contributors": [
        'Xavier ALT <xal@openerp.com>',
        'El Hadji Dem <elhadji.dem@savoirfairelinux.com>',
        'TheCloneMaster <the.clone.master@gmail.com>',
        'Sandy Carter <bwrsandman@gmail.com>',
        'Rudolf Schnapka <rs@techno-flex.de>',
        'Sebastien Alix <sebastien.alix@osiell.com>',
        'Jairo Llopis <j.llopis@grupoesoc.es>',
        'Richard deMeester <richard@willowit.com.au>',
    ],
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
