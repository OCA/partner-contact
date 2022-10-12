# Copyright 2020 Ashish (Ooops) <https://ooops404.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Mobile Format and Duplicate Checker",
    "version": "14.0.1.0.0",
    "summary": "Restriction on partner creation if another partner has the same mobile",
    "author": "Ashish Hirpara, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Partner Management",
    "depends": ["base_setup", "phone_validation"],
    "license": "AGPL-3",
    "maintainers": ["AshishHirapara"],
    "installable": True,
    "application": False,
    "data": ["views/res_config_settings_view.xml"],
}
