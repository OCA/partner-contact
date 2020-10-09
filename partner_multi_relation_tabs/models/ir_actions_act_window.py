# Copyright 2020 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class IrActionsActWindow(models.Model):
    """Make sure tabs visibility updated when loading partner forms."""

    _inherit = "ir.actions.act_window"

    @api.multi
    def read(self, fields=None, load="_classic_read"):
        """Add update_tabs_visibility if called for partner model."""
        remove_res_model = False
        if fields and "context" in fields and "res_model" not in fields:
            fields.append("res_model")
            remove_res_model = True
        result = super().read(fields=fields, load=load)
        if not fields or "context" in fields:
            for values in result:
                if values["res_model"] == "res.partner":
                    ctx = values.get("context", "{}")
                    if "update_relation_tab" not in ctx:
                        ctx = ctx.replace("{", '{"update_relation_tab": 1,  ', 1)
                        values["context"] = ctx
                if remove_res_model:
                    del values["res_model"]
        return result
