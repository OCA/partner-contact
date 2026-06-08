# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Email Duplicate Warn",
    "version": "19.0.2.1.0",
    "category": "Partner Management",
    "license": "AGPL-3",
    "summary": "Warning banner on partner form if other partners have the same email",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "assets": {
        "web.assets_backend": [
            "partner_email_duplicate_warn/static/src/components/x2many_links/x2many_links.esm.js",
            "partner_email_duplicate_warn/static/src/components/x2many_links/x2many_links.xml",
        ],
    },
    "data": [
        "views/res_partner.xml",
    ],
    "installable": True,
}
