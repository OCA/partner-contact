# Copyright (C) 2021 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Identification Notification",
    "version": "14.0.1.0.0",
    "category": "Contact",
    "depends": [
        "partner_identification",
    ],
    "author": "Open Source Integrators," "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "data": [
        "data/ir_cron_data.xml",
        "views/res_partner_id_category_view.xml",
        "views/res_partner_id_number_view.xml",
    ],
    "installable": True,
    "application": False,
}
