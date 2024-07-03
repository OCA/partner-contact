# Copyright (C) 2023 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Middle Name",
    "summary": "Have split Middle",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Open Source Integrators, " "Odoo Community Association (OCA)",
    "category": "Partner Management",
    "depends": ["partner_firstname"],
    "excludes": ["partner_second_lastname"],
    "data": ["views/res_partner.xml", "views/res_user.xml"],
    "installable": True,
}
