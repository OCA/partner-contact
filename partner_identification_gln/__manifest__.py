# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Identification Gln",
    "summary": """
        This addon extends "Partner Identification Numbers"
        to provide a number category for GLN registration""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "Acsone S.A.,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "external_dependencies": {"python": ["stdnum"]},
    "depends": ["partner_identification"],
    "data": ["data/partner_identification_gln.xml"],
    "installable": True,
}
