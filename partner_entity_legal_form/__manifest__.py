# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Partner Entity Legal Form",
    "summary": "Allows to set up legal entity from 'ISO 20275: Entity Legal Forms Code List' ",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Customer Relationship Management",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/entity.legal.form.csv",
        "data/entity.legal.form.abbreviation.csv",
        "views/res_partner_views.xml",
        "views/entity_legal_form_views.xml",
        "views/entity_legal_form_abbreviation_views.xml",
    ],
    "installable": True,
}
