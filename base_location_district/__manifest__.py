{
    "name": "Base Location District",
    "summary": "Add the disctrict field on partners",
    "version": "16.0.1.0.0",
    "category": "Partner Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Odoo Community Association (OCA), Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base_address_extended",
        "contacts",
    ],
    "data": [
        "views/res_district_views.xml",
        "views/res_partner_views.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "base_location_district/static/src/css/form_view.css",
        ]
    },
    "demo": [],
    "qweb": [],
}
