# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Identification GLN",
    "summary": "Adds a GLN registration category to Partner Identification Numbers",
    "version": "20.0.1.0.0",
    "license": "AGPL-3",
    "author": "Acsone S.A.,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_identification"],
    "data": ["data/partner_identification_gln.xml"],
    "external_dependencies": {"python": ["python-stdnum"]},
    "installable": True,
}
