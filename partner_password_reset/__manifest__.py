# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Password Reset",
    "summary": "Add Wizard to allow resetting of a Partner's associated user "
               "password from within the partner view.",
    "version": "10.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://laslabs.com/",
    "author": "LasLabs, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    'depends': [
        'auth_signup',
        'portal',
    ],
    'data': [
        'wizard/res_partner_password_reset_wizard_view.xml',
    ],
}
