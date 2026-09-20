from odoo import api, fields, models


class HREmployee(models.Model):
    _inherit = "hr.employee"

    x_employee_id = fields.Char(string="Employee ID", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("x_employee_id"):
                vals["x_employee_id"] = self.env["ir.sequence"].next_by_code(
                    "hr.employee.custom"
                )
        return super().create(vals_list)
