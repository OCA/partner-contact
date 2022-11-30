# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.tools.safe_eval import safe_eval


class IRActionsWindow(models.Model):
    _inherit = "ir.actions.act_window"

    def read(self, fields=None, context=None, load="_classic_read"):
        actions = super(IRActionsWindow, self).read(fields=fields, load=load)
        for action in filter(
            lambda rec: rec.get("res_model") == "res.partner", actions
        ):
            # By default, only show standalone contact
            action_context = safe_eval(action.get("context", "{}"))
            if "search_show_all_positions" not in action_context:
                action_context["search_show_all_positions"] = {
                    "is_set": True,
                    "set_value": False,
                }
                action.update({"context": action_context})
        return actions
