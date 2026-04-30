# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Department",
    "summary": "Adds department as a partner type",
    "version": "19.0.1.0.1",
    "category": "Customer Relationship Management",
    "author": "Odoo Community Association (OCA), ForgeFlow S.L.",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "excludes": ["partner_contact_department"],
    "data": [
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
