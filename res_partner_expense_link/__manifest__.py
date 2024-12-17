# Copyright 2024 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Res partner expense link",
    "summary": "Adds a smart button to grant direct access to their expenses",
    "version": "15.0.1.0.0",
    "category": "Expenses",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "depends": [
        "contacts",
        "hr_expense",
    ],
    "data": [
        "views/hr_expense_views.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
