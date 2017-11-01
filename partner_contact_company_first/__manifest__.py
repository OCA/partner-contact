# -*- coding: utf-8 -*-
# Copyright 2017 Andreas Stauder (brain-tec AG)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Contact Company first",
    "summary": "Prints address with company in firstname and contact person "
               "in the second line instead of Name, Company",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/partner-contact",
    "author": "brain-tec AG, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "views/base_contact_view.xml",
    ],
}
