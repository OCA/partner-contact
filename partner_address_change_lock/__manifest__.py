# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Address Change Lock",
    "summary": "Block address/country changes if unpaid invoices exist",
    "version": "16.0.1.0.0",
    "category": "contact",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["Kev-Roche"],
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "views/res_config_settings.xml",
        "views/res_partner.xml",
    ],
}
