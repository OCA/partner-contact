# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, models

from ..consts import PREDEFINED_RULES


class IRRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    def set_predefined_rules_state(self, state):
        """
        Adjust the state of predefined access rules.
        This function is designed to modify the 'active' state of predefined access rules.
        It shuts down (sets 'active' to True) or activates (sets 'active' to False)
        the rules based on the provided 'state' parameter.
        """
        rules = (
            self.with_context(active_test=False)
            .sudo()
            .search([("name", "in", PREDEFINED_RULES)])
        )
        rules.sudo().write({"active": state})
