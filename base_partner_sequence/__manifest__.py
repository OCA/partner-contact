# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2016 Camptocamp - Akim Juillerat (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "author": (
        "Tiny/initOS GmbH & Co. KG,"
        "ACSONE SA/NV,"
        "Tecnativa,"
        "Camptocamp,"
        "Odoo Community Association (OCA)"
    ),
    "name": "Add a sequence on customers' code",
    "version": "12.0.1.0.0",
    "development_status": "Stable",
    "category": "Generic Modules/Base",
    "website": "https://github.com/OCA/partner-contact",
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
