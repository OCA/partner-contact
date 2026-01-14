# Copyright 2026 Binhex - Adasat Torres de Léon
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Revenue",
    "version": "18.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "Binhex, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "data": [
        "views/res_partner_revenue_range_view.xml",
        "data/res_partner_revenue_range_data.xml",
        "views/res_partner_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "maintainers": ["adasatorres"],
}
