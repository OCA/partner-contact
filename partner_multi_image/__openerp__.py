# -*- coding: utf-8 -*-
# © 2009 Sharoon Thomas Open Labs Business Solutions
# © 2014 Serv. Tecnol. Avanzados Pedro M. Baeza
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Partners",
    "version": "9.0.1.0.0",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.tecnativa.com",
    "category": "Customer Relationship Management",
    "pre_init_hook": "pre_init_hook",
    "depends": [
        "base",
        "base_multi_image",
    ],
    "data": [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    "images": [
        "images/product.png",
        "images/db.png",
        "images/file.png",
        "images/url.png",
    ],
}
