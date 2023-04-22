# Copyright (C) 2023 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _partners_for_recalculating(self):
        return self.env["res.partner"].search(
            [
                ("is_company", "=", False),
                "|",
                "&",
                ("firstname", "!=", False),
                ("lastname", "!=", False),
                "|",
                "&",
                ("firstname", "!=", False),
                ("middlename", "!=", False),
                "&",
                ("lastname", "!=", False),
                ("middlename", "!=", False),
            ]
        )
