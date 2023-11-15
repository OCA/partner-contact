# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerCompanyType(models.Model):

    _inherit = "res.partner.company.type"

    code = fields.Char(required=True)
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one(
        "res.country.state", string="State", domain="[('country_id', '=?', country_id)]"
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique (name, country_id, code, shortcut)",
            "Partner Company Type already exists!",
        )
    ]

    @api.constrains("code", "country_id")
    def _check_unique_code_per_country(self):
        for rec in self:
            if (
                self.env["res.partner.company.type"].search_count(
                    [
                        ("code", "=", rec.code),
                        ("country_id", "!=", rec.country_id.id),
                    ]
                )
                > 1
            ):
                raise ValidationError(
                    f"Code ({rec.code}) already exists for another country!"
                )
