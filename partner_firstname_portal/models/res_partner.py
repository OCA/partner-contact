# Copyright 2025 Sylvain LE GAL (GRAP)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_frontend_writable_fields(self):
        res = super()._get_frontend_writable_fields()
        res.update({"firstname", "lastname"})
        return res

    def write(self, vals):
        if self.env.context.get("name_field_pop_value"):
            vals.pop("name", None)
        return super().write(vals)
