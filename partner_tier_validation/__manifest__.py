# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Tier Validation",
    "summary": "Support a tier validation process for Contacts",
    "version": "16.0.1.0.1",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Contact",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["contacts", "base_tier_validation", "partner_stage"],
    "data": [
        "data/tier_definition.xml",
        "views/res_partner_view.xml",
    ],
    "maintainers": ["dreispt"],
}
