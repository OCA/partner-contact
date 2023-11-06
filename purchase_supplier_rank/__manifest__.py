# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Supplier Rank",
    "summary": "Update Supplier Rank when creating a Purchase Order",
    "version": "16.0.1.0.1",
    "category": "Purchases",
    "website": "https://github.com/OCA/partner-contact",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["purchase"],
    "data": [],
    "post_init_hook": "post_init_hook",
}
