# Copyright 2024-2026 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "DEPRECATED Partner Relation Functions",
    "version": "16.0.2.0.1",
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
        # Already remove views that will clash with partner_multi_relation_contact
        # "views/res_partner_views.xml",
        "views/res_partner_relation_views.xml",
        # "views/res_partner_relation_type_views.xml",
    ],
    "auto_install": False,
    "installable": True,
    "uninstall_hook": "uninstall_hook",  # Save function data in relation_contact
}
