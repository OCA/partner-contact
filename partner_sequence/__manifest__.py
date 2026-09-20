{
    "name": "Partner & Employee Unique Sequence IDs",
    "author": "kalab.rened@outlook.com",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Custom",
    "depends": ["base", "hr", "contacts", "purchase", "sale", "purchase_request"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/res_partner_views.xml",
        "views/hr_employee_views.xml",
        "views/journal_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
    "website": "https://github.com/OCA/account-financial-tools",
}
