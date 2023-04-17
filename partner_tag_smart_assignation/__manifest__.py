# Copyright (C) 2019-2023 Compassion CH (http://www.compassion.ch)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Smart Tagger",
    "version": "13.0.1.0.0",
    "category": "Other",
    "summary": "Smart tagger, module to have smart tags who " "update themselves alone",
    "sequence": 150,
    "author": "Compassion CH, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "depends": ["base"],
    "data": ["cron/update_cron.xml", "views/smart_tagger_view.xml"],
    "installable": True,
    "auto_install": False,
}
