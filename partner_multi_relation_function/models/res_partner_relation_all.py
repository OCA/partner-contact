# Copyright 2024 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ResPartnerRelationAll(models.Model):
    """Model to show each relation from two sides."""

    _inherit = "res.partner.relation.all"

    # Override fully _rec_names_search. Not really nice, but for the moment
    # the only option. Field should be turned to a property set by a method
    # in partner_multi_relation, so would be easily extendable.
    _rec_names_search = [
        "this_partner_id.name",
        "type_selection_id.name",
        "other_partner_id.name",
        "function",
    ]

    function = fields.Char()
    allow_function = fields.Boolean(readonly=True)

    def _get_additional_relation_columns(self):
        """Get additionnal columns from res_partner_relation."""
        return super()._get_additional_relation_columns() + ", rel.function"

    def _get_additional_view_fields(self):
        """Allow inherit models to add fields to view."""
        return super()._get_additional_view_fields() + ", typ.allow_function"

    def name_get(self):
        """Add function to name if present."""
        wf = _(" with function ")  # Prevent repeated translation.
        return [
            (
                this.id,
                super(ResPartnerRelationAll, this).name_get()[0][1]
                + (this.function and wf + this.function or ""),
            )
            for this in self
        ]
