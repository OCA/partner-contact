{
    "name": "Partner Identification KYC",
    "summary": "Know Your Customer identification for partners",
    "version": "19.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": [
        "partner_identification_automation_activity",
        "partner_identification",
    ],
    "data": [
        "data/activity_type_data.xml",
        "data/identification_category_data.xml",
        "views/res_partner_views.xml",
        "views/identification_number_views.xml",
        "views/res_partner_id_category_view.xml",
    ],
    "demo": [
        "demo/identification_number_demo.xml",
    ],
    "installable": True,
    "auto_install": False,
}
