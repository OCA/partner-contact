# Copyright 2026 XCG SAS (https://orbeet.io/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Mobile Contact Only",
    "version": "19.0.1.0.0",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "summary": "Hide mobile field on company partners",
    "author": "XCG SAS, Odoo Community Association (OCA)",
    "maintainers": ["awan221"],
    "development_status": "Beta",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_mobile"],
    "data": [
        "views/res_partner.xml",
    ],
    "installable": True,
}
