# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Deduplicate Contacts ACL",
    "summary": "Contact deduplication with fine-grained permission control",
    "version": "11.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/crm_deduplicate_acl_security.xml",
        "wizards/partner_merge_view.xml",
        "views/base_partner_merge_view.xml",
    ],
    "images": [
        "images/perms.png",
    ],
}
