# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerRelationType(models.Model):

    _inherit = "res.partner.relation.type"

    allow_email = fields.Boolean(
        help="If set, the relation itself can have an email",
    )
    allow_phone = fields.Boolean(
        help="If set, the relation itself can have phone and or mobile",
    )
    allow_address = fields.Boolean(
        help="If set, the relation itself can have address data",
    )
