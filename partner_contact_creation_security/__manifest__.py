# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
	"name": "Partner Contact Creation Security",
        "summary": "Create and Edit Contacts for Existing Partners",
	"version": "12.0.1.0.0",
	"development_status": "Beta",
	"category": "Contact",
	"website":  "https://github.com/OCA/partner-contact",
        "author": "Jeff Merchant, Odoo Community Association (OCA)",
	"maintainers": ["merchantroad"],
    	"license": "AGPL-3",
	"depends": ['base'],
        "data": [
		"security/res_partner_security.xml",
		"views/res_partner_view.xml",
		],
        "application": True,
	"installable": True,
}
