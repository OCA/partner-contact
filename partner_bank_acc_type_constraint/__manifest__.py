# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bank Account Account Type Constraint",
    "version": "16.0.1.0.1",
    "category": "Partners",
    "license": "AGPL-3",
    "summary": "Adds constraint on bank account type",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/partner-contact",
    # depend on "account" only for the form view of res.partner
    "depends": ["account"],
    "data": [
        "views/res_partner.xml",
        "views/res_partner_bank.xml",
    ],
    "post_init_hook": "initialize_acc_type_manual",
    "installable": True,
}
