# Copyright 2023 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResUser(models.Model):
    _inherit = ["res.users"]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["kind"] = "user"
        self = self.with_context(skip_kind_check=True)
        return super().create(vals_list)
