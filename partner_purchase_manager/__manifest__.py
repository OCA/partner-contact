# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Partner Purchase Manager",
    "summary": "Add purchase manager field in partner",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Purchase",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["EmilioPascual"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
}
