# Copyright 2022 Mamfredy Mejia M.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Address Parish",
    "summary": "Add Parish to Cities",
    "version": "15.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_setup", "contacts", "base_address_city"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_parish_view.xml",
        "views/res_country_view.xml",
        "views/res_partner_view.xml",
    ],
}
