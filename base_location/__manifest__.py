# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018-2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Location management (aka Better ZIP)",
    "version": "15.0.1.0.3",
    "development_status": "Mature",
    "depends": ["base_address_city", "contacts"],
    "author": (
        "Camptocamp,"
        "ACYSOS S.L.,"
        "Alejandro Santana,"
        "Tecnativa,"
        "AdaptiveCity,"
        "Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "summary": """Enhanced zip/npa management system""",
    "website": "https://github.com/OCA/partner-contact",
    "data": [
        "security/ir.model.access.csv",
        "views/res_city_zip_view.xml",
        "views/res_city_view.xml",
        "views/res_country_view.xml",
        "views/res_company_view.xml",
        "views/res_partner_view.xml",
    ],
    "demo": ["demo/res_city_zip.xml"],
    "installable": True,
    "auto_install": False,
    "maintainers": ["pedrobaeza"],
}
