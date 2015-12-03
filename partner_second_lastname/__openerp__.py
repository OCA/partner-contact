# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

{
    "name": "Partner second last name",
    "summary": "Have split first and second lastnames",
    "version": "8.0.4.1.0",
    "license": "AGPL-3",
    "website": "https://grupoesoc.es",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",
    "maintainer": "Odoo Community Association (OCA)",
    "category": "Extra Tools",
    "depends": [
        "partner_firstname"
    ],
    "data": [
        "views/res_partner.xml",
        "views/res_user.xml",
    ],
    "installable": True,
    'images': [],
}
