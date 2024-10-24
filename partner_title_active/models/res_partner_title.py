# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PartnerTitle(models.Model):
    _inherit = "res.partner.title"

    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the title without removing it.",
    )
