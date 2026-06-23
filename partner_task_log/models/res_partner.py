# Copyright 2026 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    task_log_count = fields.Integer(compute="_compute_task_log_count")

    def _get_task_log_domain(self):
        self.ensure_one()
        return [
            ("active", "=", False),
            ("project_id", "=", False),
            ("parent_id", "=", False),
            ("partner_id", "=", self.id),
        ]

    def _compute_task_log_count(self):
        task_data = (
            self.env["project.task"]
            .with_context(active_test=False)
            ._read_group(
                domain=[
                    ("active", "=", False),
                    ("project_id", "=", False),
                    ("parent_id", "=", False),
                    ("partner_id", "in", self.ids),
                ],
                groupby=["partner_id"],
                aggregates=["__count"],
            )
        )
        mapped_data = {partner.id: count for partner, count in task_data}
        for partner in self:
            partner.task_log_count = mapped_data.get(partner.id, 0)

    def action_view_task_log(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "partner_task_log.action_partner_task_log"
        )
        action.update(
            {
                "display_name": self.env._(
                    "%(partner_name)s's Task Log", partner_name=self.display_name
                ),
                "domain": self._get_task_log_domain(),
                "context": {
                    "active_test": False,
                    "default_active": False,
                    "default_partner_id": self.id,
                    "default_project_id": False,
                    "default_parent_id": False,
                    "default_user_ids": [(6, 0, [self.env.uid])],
                },
            }
        )
        return action
