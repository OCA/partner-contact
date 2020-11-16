# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
	"name": "Partner Contact Creation Security",
        "summary": "Create and Edit Contacts for Existing Partners",
	"version": "1.0",
	"development_status": "Beta",
	"category": "uncategorized",
	"website":  "https://github.com/OCA/partner-contact/tree/12-oca/partner_contact_creation_security",
        "author": "Jeff Merchant, Odoo Community Association (OCA)",
	"maintainers": ["merchantroad"],
    	"license": "AGPL-3",
	"depends": ['base'],
        "data": [
		"security/contact_child_security.xml",
		"views/child_contact_creation.xml",
		],
        "application": True,
	"installable": True,
}
