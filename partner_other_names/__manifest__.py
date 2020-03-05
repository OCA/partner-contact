# -*- coding: utf-8 -*-
# Copyright 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2018 Guillermo Montoya <Github@guillermm>
# Copyright 2018 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner other names",
    "summary": "Have split first and other names",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "author": "EXA Auto Parts Github@exaap, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "category": "Partner Management",
    "depends": [
        "partner_second_lastname"
    ],
    "data": [
        "views/res_users_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
