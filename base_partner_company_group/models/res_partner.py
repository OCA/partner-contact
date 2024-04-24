# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Contact(models.Model):
    _inherit = "res.partner"

    company_group_id = fields.Many2one(
        "res.partner",
        domain=[("is_company", "=", True)],
        recursive=True,
    )
    company_group_member_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="company_group_id",
        string="Company group members",
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["company_group_id"]

    def action_view_company_group_members(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "base_partner_company_group.action_open_group_members"
        )
        all_child = self.with_context(active_test=False).search(
            [("id", "child_of", self.ids)]
        )
        action["domain"] = [("company_group_id", "in", all_child.ids)]
        return action
