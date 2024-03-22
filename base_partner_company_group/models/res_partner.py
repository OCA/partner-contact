# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Contact(models.Model):
    _inherit = "res.partner"

    company_group_id = fields.Many2one(
        "res.partner",
        string="Company group",
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
