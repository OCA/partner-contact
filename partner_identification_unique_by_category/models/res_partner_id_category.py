# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerIdCategory(models.Model):
    _inherit = "res.partner.id_category"

    has_unique_numbers = fields.Boolean(
        string="Enforce unicity",
        help="When set, duplicate numbers will not be allowed for this category.",
    )

    @api.constrains("has_unique_numbers")
    def validate_must_be_unique(self):
        for rec in self:
            if not rec.has_unique_numbers:
                continue
            ids = self.env["res.partner.id_number"].search(
                [("category_id", "in", rec.ids)]
            )
            unique_numbers = set(ids.mapped("name"))
            if len(ids) != len(unique_numbers):
                raise ValidationError(
                    _(
                        "The category {} can not be set to use unique numbers, "
                        "because it already contains duplicates."
                    ).format(rec.name)
                )
