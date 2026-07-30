# Copyright 2026 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Partner Owner Company",
    "summary": "Add owner_company_id field to contacts as soft alternative "
    "to company_id",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "maintainers": ["dreispt"],
    "depends": ["contacts"],
    "data": [
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
