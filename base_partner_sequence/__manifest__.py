# Copyright 2004-2009 Tiny SPRL (<https://tiny.be>).
# Copyright 2013 initOS GmbH & Co. KG (<https://www.initos.com>).
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2016 Camptocamp - Akim Juillerat (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "author": (
        "Tiny/initOS GmbH & Co. KG,"
        "ACSONE SA/NV,"
        "Tecnativa,"
        "Camptocamp,"
        "Odoo Community Association (OCA)"
    ),
    "name": "Add a sequence on customers' code",
    "version": "14.0.1.0.1",
    "development_status": "Production/Stable",
    "category": "Generic Modules/Base",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "summary": "Sets customer's code from a sequence",
    "data": ["data/partner_sequence.xml", "views/partner_view.xml"],
    "installable": True,
    "license": "AGPL-3",
}
