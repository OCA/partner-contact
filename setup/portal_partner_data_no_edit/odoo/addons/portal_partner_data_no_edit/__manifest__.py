# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Portal Partner Block Data Edit",
    "version": "15.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": ["portal"],
    "data": [
        "views/res_partner_views.xml",
        "views/portal_template.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "portal_partner_data_no_edit/static/src/js/portal_partner_data_no_edit_tour.js",
        ],
    },
    "installable": True,
}
