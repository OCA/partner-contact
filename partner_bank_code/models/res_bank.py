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

    def name_get(self):
        """Add bank and branch code to name if available"""
        result = super().name_get()
        return [
            (
                _id,
                name
                + (
                    (
                        " [%s%s]"
                        % (
                            self.browse(_id).bank_code,
                            ("/%s" % self.browse(_id).bank_branch_code)
                            if self.browse(_id).bank_branch_code
                            else "",
                        )
                    )
                    if self.browse(_id).bank_code
                    else ""
                ),
            )
            for _id, name in result
        ]

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """Return matches of bank_code, branch_code first"""
        matches = self.browse([])
        if name and operator not in expression.NEGATIVE_TERM_OPERATORS:
            matches = self.browse(
                self._search(
                    [
                        "|",
                        ("bank_code", "=ilike", name + "%"),
                        ("bank_branch_code", "=ilike", name + "%"),
                    ]
                    + (args or []),
                    limit=limit,
                    access_rights_uid=name_get_uid,
                )
            )
        if not limit or len(matches) < limit:
            matches += self.browse(
                super()._name_search(
                    name,
                    args=[("id", "not in", matches.ids)] + (args or []),
                    operator=operator,
                    limit=limit and limit - len(matches) or limit,
                    name_get_uid=name_get_uid,
                )
            )
        return matches.ids
