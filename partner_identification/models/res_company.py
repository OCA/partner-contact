# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    id_category_scheme_unique_check = fields.Boolean(
        string="Enforce unique ID category scheme",
        default=False,
        help="When enabled, two Partner ID Categories cannot share the "
        "same external `scheme` code.",
    )
