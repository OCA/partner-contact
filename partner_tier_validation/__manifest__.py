# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Tier Validation",
    "summary": "Extends the functionality of Contacts to"
               "support a tier validation process.",
    "version": "12.0.1.0.0",
    "category": "Contact",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "contacts",
        "base_tier_validation",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
}
