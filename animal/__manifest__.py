# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Animal",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "summary": "Manage animals information",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "maintainer": "Open Source Integrators",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["mail"],
    "data": [
        "data/ir.module.category.csv",
        "data/animal.species.csv",
        "data/animal.breed.csv",
        "data/animal.color.csv",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/animal_color.xml",
        "views/animal_breed.xml",
        "views/animal_species.xml",
        "views/animal.xml",
        "views/menu.xml",
    ],
    "application": True,
    "development_status": "Beta",
    "maintainers": ["max3903"],
}
