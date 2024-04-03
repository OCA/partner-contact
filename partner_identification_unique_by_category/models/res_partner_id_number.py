# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"
    _description = "Partner ID Number"
    _order = "name"

    @api.constrains("name", "category_id")
    def validate_id_number(self):
        result = super().validate_id_number()
        for rec in self:
            if not rec.category_id.has_unique_numbers:
                continue
            count = self.search_count(
                [("name", "=", rec.name), ("category_id", "in", rec.category_id.ids)]
            )
            if count > 1:
                raise ValidationError(
                    _(
                        "The Id {name} in the category {category} could not be created "
                        "because it already exists"
                    ).format(name=rec.name, category=rec.category_id.name)
                )
        return result
