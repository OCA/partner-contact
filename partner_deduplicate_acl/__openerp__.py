# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Deduplicate Contacts ACL",
    "summary": "Contact deduplication with fine-grained permission control",
    "version": "8.0.1.0.0",
    "category": "Tools",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm",
    ],
    "data": [
        "security/crm_deduplicate_acl_security.xml",
        "wizards/partner_merge_view.xml",
    ],
    "images": [
        "images/perms.png",
    ],
}
