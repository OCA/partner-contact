# Copyright 2023 camptocamp (<http://www.camptocamp.ch)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Partner Team",
    "version": "16.0.1.0.0",
    "category": "Contacts",
    "author": "Camptocamp, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-ux",
    "license": "AGPL-3",
    "depends": ["base", "contacts", "partner_contact_role"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_team_views.xml",
        "views/rel_team_partner_views.xml",
    ],
    "installable": True,
    "application": True,
}
