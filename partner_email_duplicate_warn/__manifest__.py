# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Email Duplicate Warn",
    "version": "16.0.1.0.0",
    "category": "Partner Management",
    "license": "AGPL-3",
    "summary": "Warning banner on partner form if another partner has the same email",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "data": [
        "views/res_partner.xml",
    ],
    "installable": True,
}
