# -*- coding: utf-8 -*-
# Copyright 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner labels",
    "version": "10.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Base",
    "summary": "Print partner labels",
    "depends": [
        'base_setup',
        'report',
    ],
    "data": [
        "views/base_config_settings.xml",
        "reports/res_partner.xml",
    ],
    "installable": True,
}
