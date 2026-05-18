# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ["user_id"]
