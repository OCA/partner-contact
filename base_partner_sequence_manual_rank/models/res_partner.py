# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _needs_ref(self, vals=None):
        if not super()._needs_ref(vals=vals):
            return False
        if vals:
            vals_for_check = vals.copy()
        else:
            vals_for_check = {}
        if "is_customer" in vals_for_check:
            return bool(vals_for_check["is_customer"])
        return False
