# Copyright 2023 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Contact -> Products with the contact's prices",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Product",
    "data": [
        "views/res_partner_views.xml",
        "views/product_product_views.xml",
    ],
    "depends": [
        "partner_stage",  # inherit header
        "product",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/partner-contact",
}
