# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Property",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "version": "20.0.1.0.0",
    "depends": ["web_tour", "bus"],
    "license": "AGPL-3",
    "category": "Partner Management",
    "data": ["views/res_partner_views.xml"],
    "assets": {
        "web.assets_backend": [
            "partner_property/static/src/partner_property.xml",
        ],
    },
    "installable": True,
    "maintainers": ["victoralmau"],
}
