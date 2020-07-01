# Copyright 2016-2020 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        """Propagate a language change in the partner to the child contacts."""
        res = super(ResPartner, self).write(vals)
        if vals.get("lang"):
            childs = self.search([("id", "child_of", self.ids), ("lang", "=", False)])
            if childs:
                childs.write({"lang": vals["lang"]})
        return res

    @api.onchange("parent_id")
    def onchange_parent_id(self):
        """Change language if the parent company changes and there's no
        language defined yet.

        A special case is made for virtual records, where default lang value
        is assigned at startup, so we always overwrite language in that case.
        """
        res = super(ResPartner, self).onchange_parent_id()
        if (
            self.parent_id.lang
            and (
                not self.lang
                or (isinstance(self.id, models.NewId) and not self._origin)
            )
            and self.parent_id.lang != self.lang
        ):
            self.lang = self.parent_id.lang
        return res
