# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Partner Routes",
    "summary": "Base module to assign routes to partners",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/partner_route_view.xml",
    ],
    "installable": True,
}
