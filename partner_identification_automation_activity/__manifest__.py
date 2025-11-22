{
    "name": "Partner Identification Automation Activity",
    "summary": "Automatically create activities when IDs need renewal",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "license": "AGPL-3",
    "author": "OBS Solutions Netherlands, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "depends": [
        "partner_identification",
        "partner_identification_automation",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_id_category_view.xml",
        "data/mail_activity_type.xml",
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}
