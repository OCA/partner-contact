# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Default sales discount per partner",
    "version": "12.0.1.0.0",
    "category": "Partner Management",
    "license": "AGPL-3",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "sale_management",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
