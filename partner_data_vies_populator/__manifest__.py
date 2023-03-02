# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Data VIES Populator",
    "summary": "Using VIES webservice, name and address information will "
    "be fetched and added to the partner.",
    "version": "14.0.1.0.3",
    "category": "Customer Relationship Management",
    "author": "NextERP Romania,"
    "Forest and Biomass Romania,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": ["base_vat"],
    "external_dependencies": {"python": ["python-stdnum"]},
    "installable": True,
}
