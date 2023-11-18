# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, models

from ..consts import PREDEFINED_RULES


class IRRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    def tweak_access_rules(self, state):
        """
        Need to shut down some non-updatable rules to ensure tweak is applied correctly
        """
        rules = (
            self.with_context(active_test=False)
            .sudo()
            .search([("name", "in", PREDEFINED_RULES)])
        )
        rules.sudo().write({"active": state})
