# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    type = fields.Selection(
        selection_add=[("department", "Department")],
        ondelete={"department": "set default"},
    )

    department_id = fields.Many2one(
        "res.partner",
        domain=[("type", "=", "department")],
    )

    department_member_ids = fields.One2many(
        "res.partner",
        "department_id",
        domain=[("type", "!=", "department")],
        string="Direct Members",
    )

    department_all_member_ids = fields.Many2many(
        "res.partner",
        compute="_compute_department_all_member_ids",
        string="Members",
    )

    department_member_count = fields.Integer(
        compute="_compute_department_member_count",
    )

    department_ids = fields.One2many(
        "res.partner",
        "parent_id",
        domain=[("type", "=", "department")],
        string="Departments",
    )

    @api.depends("department_member_ids")
    def _compute_department_all_member_ids(self):
        for dept in self:
            sub_depts = self.env["res.partner"].search(
                [("department_id", "=", dept.id), ("type", "=", "department")]
            )
            all_members = dept.department_member_ids
            for sub_dept in sub_depts:
                all_members |= sub_dept.department_member_ids
            dept.department_all_member_ids = all_members

    @api.depends("department_all_member_ids")
    def _compute_department_member_count(self):
        for partner in self:
            partner.department_member_count = len(partner.department_all_member_ids)

    def action_view_department_members(self):
        sub_depts = self.env["res.partner"].search(
            [("department_id", "=", self.id), ("type", "=", "department")]
        )
        dept_ids = [self.id] + sub_depts.ids
        return {
            "type": "ir.actions.act_window",
            "name": "Members",
            "res_model": "res.partner",
            "view_mode": "list,form",
            "domain": [
                ("department_id", "in", dept_ids),
                ("type", "!=", "department"),
            ],
            "context": {"default_department_id": self.id},
        }

    @api.constrains("parent_id", "type")
    def _check_parent_not_department(self):
        for partner in self:
            if (
                partner.parent_id
                and partner.type in ("contact", "department")
                and partner.parent_id.type == "department"
            ):
                raise ValidationError(
                    self.env._(
                        "A partner contact/department cannot have"
                        " a department as its parent."
                    )
                )
