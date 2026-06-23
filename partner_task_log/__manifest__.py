# Copyright 2026 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Partner Task Log",
    "summary": "Use project tasks without project as partner log entries",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu", "rafaelbn"],
    "license": "LGPL-3",
    "depends": [
        "project",
    ],
    "data": [
        "security/project_task_security.xml",
        "views/project_task_views.xml",
        "views/res_partner_views.xml",
    ],
}
