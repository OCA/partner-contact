# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    "name": "Partner Access Tweaks",
    "summary": "This allows to restrict contact access based on user settings",
    "version": "16.0.1.0.1",
    "category": "base",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Cetmix, Odoo Community Association (OCA)",
    "maintainers": ["CetmixGitDrone"],
    "images": ["static/description/banner.png"],
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/rules.xml",
        "data/data.xml",
        "views/res_users.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "uninstall_hook": "restore_access_rules",
}
