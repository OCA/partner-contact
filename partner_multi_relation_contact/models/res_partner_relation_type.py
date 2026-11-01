# Copyright 2026 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartnerRelationType(models.Model):

    _inherit = "res.partner.relation.type"

    allow_contact_partner = fields.Boolean(
        help="If set, allow to link connection to an address (partner) record"
        " to specify email, phone or physical address specific for the relation",
        compute="_compute_allow_contact_partner",
        store=True,
    )
    allow_email = fields.Boolean(
        help="If set, allows to specify a specific email for this relation",
    )
    allow_phone = fields.Boolean(
        help="If set, allows to specify a specific phone for this relation",
    )
    allow_address = fields.Boolean(
        help="If set, allows to specify a specific address for this relation",
    )
    allow_function = fields.Boolean(
        help="If set, relations of this type can have a function specified",
    )
    preferred_contact = fields.Selection(
        [
            ("left_partner", "Left Partner"),
            ("right_partner", "Right Partner"),
        ],
        default="right_partner",
        help="Partner to use for email, phone or address, if no contact address"
        " partner, or not set on contact address partner.",
    )
    set_contact_parent = fields.Boolean(
        default=True,
        help="Set parent on address contact to preferred partner",
    )

    @api.depends(
        "allow_email",
        "allow_phone",
        "allow_function",
        "allow_address",
    )
    def _compute_allow_contact_partner(self):
        for this in self:
            this.allow_contact_partner = (
                this.allow_email
                or this.allow_phone
                or this.allow_address
                or this.allow_function
            )
