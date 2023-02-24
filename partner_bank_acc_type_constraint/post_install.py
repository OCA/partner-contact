# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def initialize_acc_type_manual(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    bank_accounts = env["res.partner.bank"].with_context(active_test=False).search([])
    for bank_account in bank_accounts:
        bank_account.write({"acc_type_manual": bank_account.acc_type})
