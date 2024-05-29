# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner category security",
    "version": "16.0.2.0.1",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "installable": True,
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "maintainers": ["victoralmau"],
}
