# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Uom Mapping",
    "summary": "Map Odoo UoM to partner-specific UoM.",
    "version": "20.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "contacts",
        "uom",
    ],
    "data": [
        "security/partner_uom.xml",
        "views/partner_uom.xml",
    ],
}
