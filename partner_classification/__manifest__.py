# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Partner Classification",
    "summary": "Structured partner classification (alternative to tags)",
    "version": "19.0.1.0.0",
    "category": "Contacts",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "security/partner_classification_security.xml",
        "views/res_partner_classification_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
