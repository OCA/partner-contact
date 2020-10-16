# -*- coding: utf-8 -*-
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Deduplicate Contacts by reference",
    "version": "9.0.1.0.0",
    "category": "Tools",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "crm",
        "crm_deduplicate_acl",
    ],
    "data": [
        'wizards/partner_merge_view.xml',
    ],
}
