# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_address_lock_mode = fields.Selection(
        selection=[
            ("country", "Country change only"),
            ("any_address_field", "Any address field change"),
        ],
        string="Address Lock Mode",
        default="country",
        required=False,
    )
