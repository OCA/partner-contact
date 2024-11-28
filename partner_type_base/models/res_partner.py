# Copyright 2024 Christopher Rogos (<https://www.glueckkanja.com>)

from odoo import api, fields, models


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _inherit = "res.partner"

    is_address_readonly = fields.Boolean(
        compute="_compute_contact_type",
        help="If true, the address fields are readonly.",
    )
    is_individual = fields.Boolean(
        compute="_compute_contact_type", help="If true, the partner name is splitted."
    )
    can_be_parent = fields.Boolean(
        compute="_compute_contact_type",
        search="_search_can_be_parent",
        help="If true, the partner is available as parent.",
    )
    can_be_child = fields.Boolean(
        compute="_compute_contact_type",
        help="If true, the partner_id field is available.",
    )

    @api.depends("is_company", "type", "parent_id")
    def _compute_contact_type(self):
        for partner in self:
            partner.is_address_readonly = not (
                partner.is_company
                or not partner.parent_id
                or partner.type not in ["contact"]
            )
            partner.is_individual = not partner.is_company and partner.type in [
                "contact",
                "other",
            ]

            partner.can_be_parent = partner.is_company
            partner.can_be_child = not partner.is_company

    @api.model
    def _search_can_be_parent(self, operator, value):
        return [("is_company", operator, value)]
