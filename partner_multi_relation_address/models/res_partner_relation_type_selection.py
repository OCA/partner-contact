# Copyright 2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerRelationTypeSelection(models.Model):

    _inherit = "res.partner.relation.type.selection"

    allow_email = fields.Boolean(
        help="If set, the relation itself can have an email",
    )
    allow_phone = fields.Boolean(
        help="If set, the relation itself can have phone and or mobile",
    )
    allow_address = fields.Boolean(
        help="If set, the relation itself can have address data",
    )

    def _get_additional_view_fields(self):
        """Allow inherit models to add fields to view."""
        return "%s, %s" % (
            super()._get_additional_view_fields(),
            "typ.allow_email, typ.allow_phone, typ.allow_address",
        )
