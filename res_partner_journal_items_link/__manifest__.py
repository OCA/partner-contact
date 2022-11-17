# Copyright 2022 Xtendoo - Dani Domínguez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Res partner journal items link",
    "summary": "Adds a smart button to grant direct access to their accounting notes",
    "version": "15.0.1.0.0",
    "category": "Account",
    "author": "Dani Domínguez - Xtendoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": [
        "contacts",
        "account",
    ],
    "data": [
        "views/account_move_line.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
