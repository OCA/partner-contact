# Copyright 2019-2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def toggle_active(self):
        res = super().toggle_active()
        if self.env.context.get("skip_child_toggle_active"):
            return res
        for partner in self.filtered(lambda x: not x.active):
            partner.child_ids.filtered(lambda x: x.active).toggle_active()
        return res
