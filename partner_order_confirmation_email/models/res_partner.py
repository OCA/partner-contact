# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    order_confirmation_email = fields.Char(
        help=(
            "This email address will be used to send order confirmation emails. "
            "It still needs to be configured on the specific email template."
        ),
    )
