# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2019 Victor M.M Torres <victor.martin@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Exclude records from the deduplication",
    "version": "12.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "partner_deduplicate_acl",
    ],
    "data": [
        'wizards/partner_merge_view.xml',
    ],
}
