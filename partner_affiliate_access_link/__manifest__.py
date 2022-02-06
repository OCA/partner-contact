# Copyright 2022 C2i Change 2 improve <soporte@c2i.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner affiliate access link",
    "summary": "Allow to visit the full affiliate contact form from a company",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Tools",
    "website": "https://github.com/OCA/partner-contact",
    "author": "C2i Change 2 improve, Odoo Community Association (OCA)",
    "maintainers": ["emagdalenaC2i"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["partner_affiliate", "partner_contact_access_link"],
    "data": ["views/res_partner_views.xml"],
}
