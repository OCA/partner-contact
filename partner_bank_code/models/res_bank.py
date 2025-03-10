# Copyright 2021 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


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
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        domain = domain or []
        if name:
            name_domain = [
                "|",
                "|",
                "|",
                ("bic", "=ilike", name + "%"),
                ("name", operator, name),
                ("bank_code", "=ilike", name + "%"),
                ("bank_branch_code", "=ilike", name + "%"),
            ]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                name_domain = ["&", "!"] + name_domain[1:]
            domain = domain + name_domain
        return self._search(domain, limit=limit, order=order)
