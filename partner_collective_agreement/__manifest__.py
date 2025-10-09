# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Collective Agreement",
    "summary": "Collective Agreement Field for Partners.",
    "version": "18.0.1.0.0",
    "author": "Sygel, Odoo Community Association (OCA)",
    "category": "Contact",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/collective_agreement_views.xml",
        "views/res_partner_views.xml",
    ],
    "license": "LGPL-3",
}
