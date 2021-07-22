# Copyright (C) 2021 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Identification Stock",
    "version": "14.0.1.0.0",
    "category": "Stock",
    "depends": [
        "partner_identification",
        "stock",
    ],
    "author": "Open Source Integrators," "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "data": [
        "views/product_category_views.xml",
        "views/product_template_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
    "application": False,
}
