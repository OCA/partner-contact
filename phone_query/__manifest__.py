# Copyright 2025 Kencove - Mohamed Alkobrosli - (https://www.kencove.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Phone Query",
    "version": "16.0.1.0.0",
    "category": "Customer Relationship Management",
    "summary": """
        Enable the internal user of querying the partner number in browser""",
    "author": "Kencove, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "maintainers": ["Kencove"],
    "depends": ["phone_validation"],
    "data": [
        "views/query_phone_number.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "phone_query/static/src/phone_query_service.esm.js",
            "phone_query/static/src/template.xml",
            "phone_query/static/src/phone_query.esm.js",
        ],
    },
    "installable": True,
    "auto_install": False,
}
