# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Phone Format Option",
    "summary": "Choose the phone number format (with or without country code) "
    "applied on contacts",
    "version": "18.0.1.0.0",
    "category": "Contacts",
    "author": "Quartile, Odoo Community Association (OCA)",
    "maintainers": ["smorita7749"],
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": ["base_setup", "phone_validation"],
    "external_dependencies": {"python": ["phonenumbers"]},
    "data": ["views/res_config_settings_views.xml"],
    "installable": True,
}
