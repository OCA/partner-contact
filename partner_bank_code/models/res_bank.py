# Copyright 2021 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBank(models.Model):
    _inherit = "res.bank"

    bank_code = fields.Char()
    bank_branch_code = fields.Char()

    _sql_constraints = [
        (
            "bank_code_unique",
            "unique(bank_code, bank_branch_code)",
            "Bank and Branch Code should be unique.",
        ),
    ]

    def _compute_display_name(self):
        """Add bank and branch code to name if available"""
        result = super()._compute_display_name()
        return result
