# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    unique_per_organization = fields.Boolean(default=False)
