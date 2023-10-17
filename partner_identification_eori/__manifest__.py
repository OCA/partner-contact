# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Identification EORI",
    "summary": """
        This addon extends "Partner Identification Numbers"
        to provide a number category for EORI Number""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_identification"],
    "data": ["data/partner_identification_eori.xml"],
    "installable": True,
}
