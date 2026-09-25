# Copyright 2021 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    bank_code = fields.Char()
    bank_branch_code = fields.Char()

    _bank_code_unique = models.Constraint(
        "unique(bank_code, bank_branch_code)",
        "Bank and Branch Code should be unique.",
    )

    @api.depends("account_number", "bank_name", "bank_code", "bank_branch_code")
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
        if value:
            if operator in ("ilike", "not ilike"):
                domain = [
                    "|",
                    "|",
                    "|",
                    "|",
                    ("bank_bic", "=ilike", value + "%"),
                    ("bank_name", "ilike", value),
                    ("account_number", "ilike", value),
                    ("bank_code", "=ilike", value + "%"),
                    ("bank_branch_code", "=ilike", value + "%"),
                ]
                if operator == "not ilike":
                    domain = ["!", *domain]
                return domain

            domain = [
                "|",
                "|",
                "|",
                "|",
                ("bank_bic", operator, value),
                ("bank_name", operator, value),
                ("account_number", operator, value),
                ("bank_code", operator, value),
                ("bank_branch_code", operator, value),
            ]
            if operator in ("!=", "not ilike", "not like", "not in", "<>"):
                domain = ["!", *domain]
            return domain
        return super()._search_display_name(operator, value)
