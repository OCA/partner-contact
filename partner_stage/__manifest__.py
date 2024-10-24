# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Partner Stage",
    "summary": "Add lifecycle Stages to Partners",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Sales/CRM",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/partner_stage_data.xml",
        "views/res_partner_stage_views.xml",
        "views/res_partner_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "maintainers": ["dreispt"],
}
