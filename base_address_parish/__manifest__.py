# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016-2017 Tecnativa S.L. - Vicent Cubells
# Copyright 2019 Tecnativa S.L. - Cristina Martin R.
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
