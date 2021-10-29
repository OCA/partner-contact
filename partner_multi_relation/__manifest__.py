# Copyright 2013-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Relations",
    "version": "12.0.1.2.2",
    "author": "Therp BV,Camptocamp,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "depends": [
        "contacts",
        "web_domain_field",
        "web_tree_many2one_clickable",
    ],
    "demo": [
        "demo/res_partner_category_demo.xml",
        "demo/res_partner_demo.xml",
        "demo/res_partner_relation_type_demo.xml",
        "demo/res_partner_relation_demo.xml",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_relation.xml",
        "views/res_partner_relation_all.xml",
        "views/res_partner.xml",
        "views/res_partner_relation_type.xml",
        "views/menu.xml",
    ],
    "auto_install": False,
    "installable": True,
}
