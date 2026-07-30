# Copyright 2024-2026 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerRelation(models.Model):

    _inherit = "res.partner.relation"

    contact_function = fields.Char()
    allow_function = fields.Boolean(
        readonly=True,
        related="type_id.allow_function",
    )
