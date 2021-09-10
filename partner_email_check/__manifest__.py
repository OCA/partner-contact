# Copyright 2019 Komit <https://komit-consulting.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Email Format Checker",
    "version": "14.0.1.1.1",
    "summary": "Validate email address field",
    "author": "Komit, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Tools",
    "depends": ["base_setup"],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
    "external_dependencies": {"python": ["email-validator"]},
    "data": ["views/base_config_view.xml"],
    "demo": ["demo/res_company_demo.xml"],
}
