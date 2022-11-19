# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "City districts",
    "summary": "Manage the city district of an address",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    'category': 'Base',
    "website": "https://github.com/OCA/partner-contact",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base_address_city",
    ],
    "data": [
        "views/res_city.xml",
        "views/res_city_district.xml",
        "security/ir.model.access.csv",
    ],
}
