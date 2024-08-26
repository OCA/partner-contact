# Copyright 2024 Trobz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Classification",
    "summary": "This module is used to classify partners",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "author": "Trobz, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "website": "https://github.com/OCA/partner-contact",
    "images": ["static/description/banner.png"],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_view.xml",
        "views/partner_classification_view.xml",
    ],
}
