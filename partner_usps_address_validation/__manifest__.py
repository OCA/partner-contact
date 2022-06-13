# Copyright 2022 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "USPS Address Validation",
    "category": "Contact",
    "version": "14.0.1.0.0",
    "summary": """Utilize the USPS open API for address validation""",
    "depends": ["contacts"],
    "external_dependencies": {"python": ["xmltodict", "requests"]},
    "data": [
        "security/ir.model.access.csv",
        "wizard/usps_address_validation.xml",
        "views/res_partner.xml",
        "views/config.xml",
    ],
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "maintainer": ["ckolobow"],
    "website": "https://github.com/OCA/sale-workflow",
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "AGPL-3",
}
