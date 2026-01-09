# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Title",
    "version": "19.0.1.0.0",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "summary": "Add title field on partner",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "development_status": "Beta",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_title.xml",
        "views/res_partner.xml",
        "data/res_partner_title.xml",
    ],
    "demo": ["demo/res_partner.xml"],
    "installable": True,
}
