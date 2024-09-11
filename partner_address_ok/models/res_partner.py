# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    address_ok = fields.Boolean(
        "Addess is OK",
        copy=False,
        default=False,
        help="The address is ok if it is a valid postal address.",
    )
