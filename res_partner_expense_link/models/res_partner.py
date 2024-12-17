# Copyright 2024 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    expense_sheet_count = fields.Integer(
        compute="_compute_expense_count",
    )

    def _compute_expense_count(self):
        Employee = self.env["hr.employee"].sudo()
        Sheet = self.env["hr.expense.sheet"].sudo()

        employees = Employee.search([("address_home_id", "in", self.ids)])

        partner_employees = {}
        for emp in employees:
            partner_employees.setdefault(emp.address_home_id.id, []).append(emp.id)

        if employees:
            data = Sheet.read_group(
                [("employee_id", "in", employees.ids)], ["employee_id"], ["employee_id"]
            )
            employee_count = {d["employee_id"][0]: d["employee_id_count"] for d in data}
        else:
            employee_count = {}

        for partner in self:
            partner.expense_sheet_count = sum(
                employee_count.get(emp_id, 0)
                for emp_id in partner_employees.get(partner.id, [])
            )

    def action_view_expense_sheets(self):
        self.ensure_one()

        Employee = self.env["hr.employee"].sudo()

        employees = Employee.search([("address_home_id", "=", self.id)])

        return {
            "name": "Expense Sheets",
            "type": "ir.actions.act_window",
            "res_model": "hr.expense.sheet",
            "view_mode": "tree,form",
            "domain": [("employee_id", "in", employees.ids)],
        }
