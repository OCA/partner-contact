# -*- coding: utf-8 -*-
# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
# Copyright 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Add a sequence on customers' code",
    "version": "9.0.0.1.0",
    "author": "Tiny/initOS GmbH & Co. KG,"
              "ACSONE SA/NV,"
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "category": "Generic Modules/Base",
    "website": "http://www.initos.com",
    "depends": [
        'base',
    ],
    "summary": "Sets customer's code from a sequence",
    "data": [
        'data/partner_sequence.xml',
        'views/partner_view.xml',
    ],
    "installable": True,
    "license": "AGPL-3",
}
