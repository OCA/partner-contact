{
    "name": "Partner QR Code",
    "version": "17.0.1.0.0",
    "category": "Contacts",
    "author": "`Exo Software <https://exosoftware.pt>`_, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/partner_qr_data.xml",
        "wizard/contacts_qr_code_views.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
