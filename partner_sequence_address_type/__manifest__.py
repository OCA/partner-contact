{
    "name": "Partner Sequence Address Type",
    "version": "14.0.1.0.0",
    "depends": [
        "base_partner_sequence",
        "contacts",
    ],
    "author": "PyTech SRL, Ooops404, Odoo Community Association (OCA)",
    "maintainers": ["aleuffre", "renda-dev", "PicchiSeba"],
    "website": "https://github.com/OCA/partner-contact",
    "category": "Partner Management",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/ir_sequence_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
