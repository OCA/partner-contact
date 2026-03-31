# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        if self.env.context.get("name_field_pop_value"):
            vals.pop("name", None)
        return super().write(vals)
