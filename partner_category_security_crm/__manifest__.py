# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner category security (crm extension)",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["partner_category_security", "crm"],
    "installable": True,
    "auto_install": True,
    "data": [
        "security/ir.model.access.csv",
    ],
    "maintainers": ["victoralmau"],
}
