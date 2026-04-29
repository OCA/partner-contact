# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
    def _compute_department_member_count(self):
        for partner in self:
            partner.department_member_count = len(partner.department_member_ids)

    def action_view_department_members(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Members",
            "res_model": "res.partner",
            "view_mode": "list,form",
            "domain": [("department_id", "=", self.id)],
            "context": {"default_department_id": self.id},
        }
