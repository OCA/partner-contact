# Copyright 2024 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Relation Functions",
    "version": "16.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "maintainers": ["NL66278"],
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "depends": ["partner_multi_relation"],
    "demo": [
        "demo/res_partner_relation_type_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/res_partner_relation_demo.xml",  # Must be after type and partner
    ],
    "data": [
        "views/res_partner_relation_all_views.xml",
        "views/res_partner_relation_type_views.xml",
    ],
    "auto_install": False,
    "installable": True,
}
