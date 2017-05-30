# -*- coding: utf-8 -*-
# © 2016 Tecnativa, S.L. - Jairo Llopis
# © 2016 Tecnativa, S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Deduplicate Contacts ACL",
    "summary": "Contact deduplication with fine-grained permission control",
    "version": "10.0.1.0.0",
    "category": "Tools",
    "website": "http://www.tecnativa.com",
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
