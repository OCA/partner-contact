# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner last name uppercase",
    "summary": "Uppercases the the last names of partners",
    "version": "16.0.1.0.1",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainer": "Coop IT Easy SC",
    "category": "Extra Tools",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_firstname"],
    "data": [
        "data/actions.xml",
        "views/res_config_settings.xml",
    ],
}
