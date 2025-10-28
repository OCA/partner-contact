# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Mobile",
    "version": "19.0.1.0.0",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "summary": "Add mobile field on partner",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "development_status": "Beta",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "data": [
        "views/res_partner.xml",
    ],
    "demo": ["demo/res_partner.xml"],
    "installable": True,
}
