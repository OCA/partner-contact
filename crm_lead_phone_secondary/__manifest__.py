# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Secondary phone number on leads",
    "summary": "Adds a secondary phone number on CRM leads",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "category": "Customer Relationship Management",
    "depends": ["crm", "partner_phone_secondary"],
    "website": "https://github.com/OCA/partner-contact",
    "data": ["views/crm_lead.xml"],
    "installable": True,
}
