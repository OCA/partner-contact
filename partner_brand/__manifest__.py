# Copyright (C) 2019 Open Source Integrators
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Brand",
    "summary": "Manage your brands and use them on your documents",
    "version": "12.0.2.0.0",
    "category": "Sales Management",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Open Source Integrators,"
              "ACSONE SA/NV,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "contacts",
    ],
    "data": [
        'security/res_brand.xml',
        'views/res_brand.xml',
        "views/report_template.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["osi-scampbell"],
}
