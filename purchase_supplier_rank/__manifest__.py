# Copyright 2023 Álvaro Marcos <alvaro.marcos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Supplier Rank",
    "summary": "Update Supplier Rank when creating a Purchase Order",
    "version": "16.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Factorlibre, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["purchase"],
    "data": [],
    "post_init_hook": "post_init_hook",
}
