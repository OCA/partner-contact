# Copyright 2022 ONESTEIN (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Base Municipality",
    "summary": "Manage municipality informations on contacts",
    "version": "15.0.1.0.0",
    "category": "Partner Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "contacts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_country_municipality_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "menuitems.xml",
    ]
}
