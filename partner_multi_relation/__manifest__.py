# Copyright 2013-2025 Therp BV <http://therp.nl>.
# Copyright 2026 Open Eye Development <http://openeyedev.eu>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Relations",
    "version": "20.0.1.0.0",
    "author": "Therp BV"
    ",Camptocamp"
    ",Open Eye Development"
    ",Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "depends": ["contacts", "sales_team"],
    "demo": ["data/demo.xml"],
    "data": [
        "security/ir.access.csv",
        "views/res_partner_relation_type.xml",
        "views/res_partner_relation.xml",
        "views/res_partner.xml",
        "views/ir_actions_act_window.xml",
        "views/menu.xml",
    ],
    "auto_install": False,
    "installable": True,
}
