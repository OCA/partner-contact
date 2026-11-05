# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def default_get(self, fields):
        # is_company is inherited from res.partner: a context default is read
        # here and would not go through res.partner.default_get.
        res = super().default_get(fields)
        res.pop("is_company", None)
        return res
