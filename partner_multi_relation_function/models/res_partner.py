# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models
from odoo.osv.expression import FALSE_LEAF


class ResPartner(models.Model):
    """Enable searching partner via function"""

    _inherit = "res.partner"

    search_relation_function = fields.Many2one(
        comodel_name="res.partner.relation.all",
        compute=lambda self: self.update({"search_relation_function": None}),
        search="_search_relation_function",
        string="Has relation function",
    )

    @api.model
    def _search_relation_function(self, operator, value):
        """Search partners based on their relation function."""
        SUPPORTED_OPERATORS = (
            "=",
            "!=",
            "like",
            "not like",
            "ilike",
            "not ilike",
            "in",
            "not in",
        )
        if operator not in SUPPORTED_OPERATORS:
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator
            )
        relation_model = self.env["res.partner.relation.all"]
        relation_function_selection = relation_model.search(
            [
                ("function", operator, value),
            ]
        )
        if not relation_function_selection:
            return [FALSE_LEAF]
        # Collect both partners, user can apply
        # additional type filter for separating contacts
        # and companies
        return [("relation_all_ids", "in", relation_function_selection.ids)]
