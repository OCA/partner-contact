# Copyright 2023 NathanQj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Google Reviews",
    "summary": """
        Integrates Google Reviews into Odoo Contacts
        """,
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Akretion, NathanQj",
    "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "base_geolocalize",
    ],
    "data": [
        "views/res_config_settings_view.xml",
        "views/partner_view.xml",
    ],
    "demo": [],
}
