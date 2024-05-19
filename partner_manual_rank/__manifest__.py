# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Manual Rank",
    "summary": "Be able to manually flag partners as customer or supplier.",
    "version": "14.0.1.2.0",
    "category": "Partner Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account"],
    "data": ["views/res_partner.xml"],
    "pre_init_hook": "pre_init_hook",
}
