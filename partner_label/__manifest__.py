# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner labels",
    "version": "12.0.1.1.0",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Base",
    "summary": "Print partner labels",
    "depends": [
        'base_setup',
    ],
    "data": [
        "views/base_config_settings.xml",
        "reports/res_partner.xml",
    ],
    "installable": True,
}
