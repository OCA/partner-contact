# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Contact's Age Range",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "author": "Druidoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Customer Relationship Management",
    "summary": "Age Range for Contact's",
    "depends": ["contacts", "partner_contact_birthdate"],
    "data": [
        "security/ir.model.access.csv",
        "data/age_range_cron.xml",
        "views/res_partner_view.xml",
        "views/res_partner_age_range_view.xml",
    ],
    "installable": True,
}
