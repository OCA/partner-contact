# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Customer Rank",
    "summary": "Update Customer Rank when creating a Sale Order",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/partner-contact",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_management"],
    "data": [],
    "post_init_hook": "post_init_hook",
}
