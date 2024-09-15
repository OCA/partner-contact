# Copyright 2024 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerRelationTypeSelection(models.Model):

    _inherit = "res.partner.relation.type.selection"

    allow_function = fields.Boolean()

    def _get_additional_view_fields(self):
        """Add allow_function to fields."""
        return super()._get_additional_view_fields() + ", allow_function"
