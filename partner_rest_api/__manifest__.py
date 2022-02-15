# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Rest Api",
    "summary": """Add a REST API to manage partners""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base_rest", "base_rest_pydantic", "extendable"],
    "data": [],
    "external_dependencies": {
        "python": [
            "extendable-pydantic",
        ]
    },
}
