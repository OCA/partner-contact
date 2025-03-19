# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner address history",
    "summary": "Keep history of address changes",
    "version": "15.0.1.0.0",
    "category": "Generic Modules/Base",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_setup"],
    "data": [
        "security/partner_security.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/res_partner_history_views.xml",
        "views/res_partner_views.xml",
    ],
    "development_status": "Alpha",
    "maintainers": ["Saran440"],
}
