# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Contact(models.Model):
    _inherit = "res.partner"

    company_group_id = fields.Many2one(
        "res.partner", "Company group", domain=[("is_company", "=", True)]
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["company_group_id"]
