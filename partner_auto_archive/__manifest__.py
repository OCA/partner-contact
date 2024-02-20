# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Auto Archive",
    "version": "16.0.1.0.0",
    "author": "ForgeFlow,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Customer Relationship Management",
    "summary": "Archive periodically all contacts marked as auto-archive.",
    "license": "AGPL-3",
    "depends": [
        "base",
    ],
    "data": ["views/res_partner_views.xml", "data/ir_cron.xml"],
    "installable": True,
    "application": False,
}
