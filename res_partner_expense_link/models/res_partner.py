# Copyright 2024 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    expense_sheet_count = fields.Integer(
        compute="_compute_expense_count",
    )

    def _compute_expense_count(self):
        sheet_model = self.env["hr.expense.sheet"]
        employee_model = self.env["hr.employee"]
        for partner in self:
            employee_partner = employee_model.search_read(
                domain=[("address_home_id", "=", partner.id)], fields=["id"]
            )
            # Skip if no employee link to this partner
            if not employee_partner:
                partner.expense_sheet_count = 0
                continue

            expense_link = sheet_model.search_count(
                [("employee_id", "=", employee_partner[0]["id"])]
            )
            partner.expense_sheet_count = expense_link
