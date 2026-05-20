# Copyright 2025 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Archive Propagate",
    "summary": "Archive/unarchive partner contacts hierarchically",
    "version": "16.0.1.1.0",
    "category": "Partner Management",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
        "wizard/archive_propagate_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "maintainers": ["ntsirintanis"],
}
