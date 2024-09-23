#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Name History",
    "summary": "Save the changes to partner name.",
    "author": "Davide Corio, Odoo Community Association (OCA)",
    "maintainers": [
        "SirAionTech",
    ],
    "website": "https://github.com/OCA/partner-contact",
    "category": "Customer Relationship Management",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_name_history_views.xml",
        "views/partner_views.xml",
    ],
}
