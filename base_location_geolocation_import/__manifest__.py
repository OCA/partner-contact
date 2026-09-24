# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Import geolocation (latitude and longitude) linked to zip",
    "version": "18.0.1.0.0",
    "maintainers": ["NL66278"],
    "depends": [
        "base_geolocalize",
        "base_location_geonames_import",
    ],
    "author": ("Therp BV," "Odoo Community Association (OCA)"),
    "license": "AGPL-3",
    "summary": "Import geolocation (latitude and longitude) with geonames",
    "website": "https://github.com/OCA/partner-contact",
    "data": [
        "views/res_city_zip_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
