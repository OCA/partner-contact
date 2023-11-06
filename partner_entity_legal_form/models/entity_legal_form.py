# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EntityLegalForm(models.Model):
    _name = "entity.legal.form"
    _description = "Entity Legal Form Model"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    country_id = fields.Many2one("res.country", string="Country", required=True)
    state_id = fields.Many2one(
        "res.country.state", string="State", domain="[('country_id', '=?', country_id)]"
    )
    comment = fields.Text(string="Notes")

    abbreviation_ids = fields.One2many(
        "entity.legal.form.abbreviation",
        "entity_legal_form_id",
        string="Abbreviations",
    )

    @api.constrains("code", "country_id")
    def _check_unique_code_per_country(self):
        for rec in self:
            if (
                self.env["entity.legal.form"].search_count(
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
