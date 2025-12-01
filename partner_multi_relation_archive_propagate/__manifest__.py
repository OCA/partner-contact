# Copyright 2025 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Multi Relation Archive Propagate",
    "summary": "Propagate archiving via partner_multi_relation relations",
    "version": "16.0.1.0.0",
    "category": "Partner Management",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": [
        "partner_multi_relation",
        "partner_archive_propagate",
    ],
    "data": [
        "views/partner_relation_type_views.xml",
    ],
    "installable": True,
    "application": False,
    "maintainers": ["ntsirintanis"],
}
