# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Partner Interest Group",
    "summary": """
        Add Interest Group to Partners""",
    "version": "16.0.1.2.0",
    "category": "Partner",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": ["contacts"],
    "excludes": [],
    "data": [
        "views/res_partner_interest_group_view.xml",
        "views/res_partner_view.xml",
        "security/ir.model.access.csv",
        "security/interest_group_rules.xml",
    ],
    "demo": [],
    "qweb": [],
}
