# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Enforce IBAN Validation",
    "summary": "Enforce IBAN validation for partners",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Cetmix OÜ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "contacts",
        "base_iban",
    ],
    "data": [
        "views/res_config_settings_view.xml",
    ],
    "application": False,
    "installable": True,
}
