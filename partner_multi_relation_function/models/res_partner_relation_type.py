# Copyright 2024 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerRelationType(models.Model):

    _inherit = "res.partner.relation.type"

    allow_function = fields.Boolean(
        help="Is set, relations of this type can have a function specified",
    )
