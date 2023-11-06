# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2015 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partners Capital",
    "version": "16.0.0.1.1",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "Antiun Ingeniería S.L., "
    "Tecnativa, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["contacts"],
    "data": [
        "views/res_partner_turnover_range_view.xml",
        "views/res_partner_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "maintainers": ["EmilioPascual"],
}
