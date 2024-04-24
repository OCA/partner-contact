# Copyright 2024 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerRelation(models.Model):

    _inherit = "res.partner.relation"

    function = fields.Char()

    @api.constrains("function")
    def _check_function(self):
        """Function should only be filled when allowed on type."""
        for record in self:
            if record.function and not record.type_id.allow_function:
                raise ValidationError(
                    _("You can not have a function on relations of type %(type)s."),
                    {"type": record.type_id.display_name},
                )
