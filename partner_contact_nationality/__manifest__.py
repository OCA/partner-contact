# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact nationality",
    "summary": "Add nationality field to contacts",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://odoo-community.org/",
    "author": "Grupo ESOC, Odoo Community Association (OCA)",
    "contributors": [
        'Jairo Llopis <j.llopis@grupoesoc.es>',
        'Richard deMeester <richard@willowit.com.au>',
        'Denis Roussel <denis.roussel@acsone.eu>',
    ],
    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "partner_contact_personal_information_page",
    ],
    "data": [
        "views/res_partner.xml",
    ],
}
