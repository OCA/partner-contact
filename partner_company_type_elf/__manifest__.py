# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Partner Company Type ELF",
    "summary": "Allows to set up legal entities from 'ISO 20275: Entity Legal Forms Code List'",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow S.L., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["partner_company_type"],
    "data": [
        "views/res_partner_company_type.xml",
        "data/res.partner.company.type.csv",
    ],
    "installable": True,
    "application": False,
    "pre_init_hook": "pre_init_hook",
}
