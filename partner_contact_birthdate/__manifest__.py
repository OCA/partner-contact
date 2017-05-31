# -*- coding: utf-8 -*-
# Copyright 2014-2015  Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact's birthdate",
    "version": "10.0.1.1.0",
    "author": "Tecnativa,"
              "Odoo Community Association (OCA)",
    "category": "Customer Relationship Management",
    "website": "https://www.tecnativa.com/",
    "depends": [
        "partner_contact_personal_information_page",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "post_init_hook": "post_init_hook",
    "license": "AGPL-3",
    'installable': True,
}
