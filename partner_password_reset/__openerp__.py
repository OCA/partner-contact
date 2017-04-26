# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Password Reset",
    "summary": "Add Action to allow resetting of a Partner's associated user "
               "password from within the partner view.",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://laslabs.com/",
    "author": "LasLabs, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    'depends': [
        'auth_signup',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
}
