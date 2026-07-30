# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner First Name and Last Name - Auth Signup",
    "summary": "Glue module to make working auth signup and partner firstname module"
    " together",
    "version": "18.0.1.0.0",
    "author": "GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "category": "Extra Tools",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_firstname", "partner_is_company_auth_signup", "auth_signup"],
    "data": ["views/auth_signup_login_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "partner_firstname_auth_signup/static/src/**/*",
        ],
    },
    "auto_install": True,
}
