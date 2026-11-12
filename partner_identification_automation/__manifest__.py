{
    "name": "Partner Identification Numbers Automation",
    "summary": "Automate partner identification numbers status updates "
    "and default values",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "OBS Solutions Netherlands, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "base",
        "partner_identification",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_id_category_view.xml",
        "data/cron.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}
