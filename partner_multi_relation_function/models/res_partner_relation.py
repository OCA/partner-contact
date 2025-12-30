# Copyright 2024-2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):

    _inherit = "res.partner.relation"

    function = fields.Char()
    allow_function = fields.Boolean(
        readonly=True,
        related="type_id.allow_function",
    )

    @api.constrains("function")
    def _check_function(self):
        """Function should only be filled when allowed on type."""
        for this in self:
            if this.function and not this.type_id.allow_function:
                raise ValidationError(
                    _("You can not have a function on relations of type %(type)s."),
                    {"type": this.type_id.display_name},
                )

    def name_get(self):
        """Add function to name if present."""
        wf = _(" with function ")  # Prevent repeated translation.
        return [
            (
                this.id,
                super(ResPartnerRelation, this).name_get()[0][1]
                + (this.function and wf + this.function or ""),
            )
            for this in self
        ]
