# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner contact birthplace",
    "summary": "This module allows to define a birthplace for partners.",
    "version": "14.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "partner_contact_personal_information_page",
    ],
    "data": ["views/res_partner.xml"],
}
