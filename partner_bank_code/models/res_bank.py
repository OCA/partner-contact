# Copyright 2021 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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

    @api.depends("name", "bank_code", "bank_branch_code")
    def _compute_display_name(self):
        """Compute display name with bank code and branch code."""
        res = super()._compute_display_name()
        for rec in self:
            if not rec.bank_code:
                continue

            display_parts = f"{rec.display_name} [{rec.bank_code}"
            if rec.bank_branch_code:
                display_parts += f"/{rec.bank_branch_code}"
            display_parts += "]"
            rec.display_name = display_parts
        return res

    @api.model
    def _search_display_name(self, operator, value):
        if operator in ("ilike", "not ilike") and value:
            domain = [
                "|",
                "|",
                "|",
                ("bic", "=ilike", value + "%"),
                ("name", "ilike", value),
                ("bank_code", "=ilike", value + "%"),
                ("bank_branch_code", "=ilike", value + "%"),
            ]
            if operator == "not ilike":
                domain = ["!", *domain]
            return domain
        return super()._search_display_name(operator, value)
