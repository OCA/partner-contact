# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _mobile_get_number_fields(self):
        if "mobile" in self:
            return ["mobile"]
        else:
            return []
