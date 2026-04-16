# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner Order Confirmation Email",
    "version": "19.0.1.0.0",
    "category": "Partner",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "summary": """
        Add a specific email address for order confirmation emails on res.partner
    """,
    "depends": ["contacts"],
    "data": [
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
