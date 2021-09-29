# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Identification DEA",
    "category": "Customer Relationship Management",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["partner_identification", "sale"],
    "data": [
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "data/res_partner_id_category_data.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    "author": "Open Source Integrators (OSI)," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "maintainer": "Open Source Integrators",
    "development_status": "Production/Stable",
}
