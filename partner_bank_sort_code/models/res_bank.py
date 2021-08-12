# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBank(models.Model):

    _inherit = "res.bank"

    sort_code = fields.Char()

    _sql_constraints = [
        (
            "sort_code_unique",
            "EXCLUDE (sort_code WITH =) WHERE (active = True)",
            "Sort Code has to be unique",
        ),
    ]
