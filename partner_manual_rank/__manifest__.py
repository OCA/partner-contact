# Copyright 2021 ForgeFlow S.L.
# Copyright 2022 Vauxoo, S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Manual Rank",
    "summary": "Be able to manually flag partners as customer or supplier.",
    "version": "18.0.1.1.0",
    "category": "Partner Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "ForgeFlow, Vauxoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "maintainers": ["luisg123v", "frahikLV"],
    "depends": ["account"],
    "data": [
        # Data
        "data/ir_config_parameter.xml",
        # Views
        "views/res_partner.xml",
        "views/res_config_settings_view.xml",
    ],
}
