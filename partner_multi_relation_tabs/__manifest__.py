# Copyright 2014-2018 Therp BV <https://therp.nl>.

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Show partner relations in own tab",
    "version": "12.0.2.0.0",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "depends": ["partner_multi_relation"],
    "demo": [
        "demo/res_partner_category_demo.xml",
        "demo/res_partner_tab_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/res_partner_relation_type_demo.xml",
        "demo/res_partner_relation_demo.xml",
    ],
    "data": [
        "views/res_partner_tab.xml",
        "views/res_partner_relation_type.xml",
        "views/res_partner_relation_all.xml",
        "views/menu.xml",
        "security/ir.model.access.csv",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
