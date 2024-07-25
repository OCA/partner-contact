# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL-3.0)

{
    "name": "Partner Category Description",
    "summary": """Adds a description field to contact categories to improve
    organization and managment of customer relationships.""",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Marketing",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["edlopen", "rafaelbn"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "contacts",
    ],
    "data": [
        "views/res_partner_category_views.xml",
    ],
}
