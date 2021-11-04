{
    "name": "Phone Validation Configuration",
    "summary": "Configure format and exceptions for phone numbers",
    "version": "14.0.1.0.0",
    "development_status": "Production/Stable",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Le Filament, Odoo S.A., Odoo Community Association (OCA)",
    "maintainers": ["remi-filament"],
    "license": "GPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "phone_validation",
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
