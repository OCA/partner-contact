# Copyright 2025 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerRelationAll(models.Model):
    """Model to show each relation from two sides."""

    _inherit = "res.partner.relation.all"

    email = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    street = fields.Char()
    zipcode = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one(comodel_name="res.country")
    allow_email = fields.Boolean(readonly=True)
    allow_phone = fields.Boolean(readonly=True)
    allow_address = fields.Boolean(readonly=True)

    def _get_additional_relation_columns(self):
        """Get additionnal columns from res_partner_relation."""
        return "%s, %s, %s, %s" % (
            super()._get_additional_relation_columns(),
            "rel.email",
            "rel.phone, rel.mobile",
            "rel.street, rel.zipcode, rel.city, rel.country_id",
        )

    def _get_additional_view_fields(self):
        """Allow inherit models to add fields to view."""
        return "%s, %s" % (
            super()._get_additional_view_fields(),
            "typ.allow_email, typ.allow_phone, typ.allow_address",
        )
