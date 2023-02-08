{
    "name": "Merge Duplicate Contacts",
    "category": "Merge Duplicate Contacts",
    "version": "15.0.1.0.0",
    "author": "Nitrokey GmbH," "Odoo Community Association (OCA)",
    "summary": """Merge duplicate partner contact separated by partner fields.""",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/partner-contact",
    "sequence": "1",
    "depends": ["base", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/merge_contact_view.xml",
    ],
}
