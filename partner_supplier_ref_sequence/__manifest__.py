# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner Supplier Reference Sequence",
    "summary": "Adds a sequence for the Supplier Reference field",
    "version": "18.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["partner_supplier_ref", "partner_manual_rank"],
    "data": ["data/partner_sequence.xml"],
}
