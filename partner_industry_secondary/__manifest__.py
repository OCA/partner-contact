# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2016-2017 Tecnativa S.L. - Vicent Cubells
# Copyright 2019 Tecnativa S.L. - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Industry Secondary",
    "summary": "Add secondary partner industries",
    "version": "12.0.1.0.1",
    "category": "Sales",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_setup", "contacts",],
    "data": [
        "security/ir.model.access.csv",
        "security/partner_industry_security.xml",
        "views/res_partner_industry_view.xml",
        "views/res_partner_view.xml",
        "views/res_config_settings.xml",
    ],
}
