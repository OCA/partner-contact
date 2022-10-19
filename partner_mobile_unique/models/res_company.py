# Copyright 2022 Ooops, Ashish Hirpara
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_mobile_unique_filter_duplicates = fields.Boolean(
        string="Filter duplicate partner moblie number",
        help="Don't allow multiple partners to have the same moblie number.",
    )
