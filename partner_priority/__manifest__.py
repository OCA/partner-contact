# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner Priority",
    "summary": "Adds priority to partners.",
    "author": "Patrick Wilson, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "category": "Customer Relationship Management",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "views/res_partner.xml",
        "views/partner_priority.xml",
        "security/ir.model.access.csv",
        "data/partner_priority_data.xml",
        "data/partner_priority_sequence_data.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["patrickrwilson"],
}
