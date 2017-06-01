# -*- coding: utf-8 -*-
# Copyright 2009 Sharoon Thomas Open Labs Business Solutions
# Copyright 2014 Tecnativa - Pedro M. Baeza
# Copyright 2015 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2016 Sodexis
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Partners",
    "version": "9.0.1.0.0",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://www.tecnativa.com",
    "category": "Customer Relationship Management",
    "pre_init_hook": "pre_init_hook",
    "uninstall_hook": "uninstall_hook",
    "depends": [
        "base",
        "base_multi_image",
    ],
    "data": [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
