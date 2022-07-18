# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Uom Mapping",
    "summary": """
        This module adds a mapping table between the unit of measure defined in
         Odoo and a partner side one.""",
    "version": "14.0.1.0.0",
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
