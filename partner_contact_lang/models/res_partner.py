# Copyright 2016-2020 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        """Propagate a language change in the partner to the child contacts."""
        res = super().write(vals)
        if vals.get("lang"):
            childs = self.search([("id", "child_of", self.ids), ("lang", "=", False)])
            if childs:
                childs.write({"lang": vals["lang"]})
        return res

    def _compute_lang(self):
        if self.lang:
            return
        super()._compute_lang()
