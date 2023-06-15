# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerDateRange(models.Model):
    _name = "res.partner.age.range"
    _description = "Partner Age Range"

    def _default_age_from(self):
        age_from = 0
        last_age_range = self.env["res.partner.age.range"].search(
            [], order="age_to desc", limit=1
        )
        if last_age_range:
            age_from = last_age_range.age_to + 1
        return age_from

    name = fields.Char(required=True)
    age_from = fields.Integer(
        string="From", required=True, default=lambda self: self._default_age_from()
    )
    age_to = fields.Integer(string="To", required=True)

    _sql_constraints = [("name_uniq", "unique (name)", "A name must be unique !")]

    @api.constrains("age_from", "age_to")
    def _validate_range(self):
        for rec in self:
            if rec.age_from >= rec.age_to:
                raise ValidationError(
                    _(
                        "%(name)s is not a valid range (%(age_from)s >= %(age_to)s)",
                        name=rec.name,
                        age_from=rec.age_from,
                        age_to=rec.age_to,
                    )
                )
            range_id = rec.search(
                [
                    ("age_from", "<=", rec.age_to),
                    ("age_to", ">=", rec.age_from),
                    ("id", "!=", rec.id),
                ],
                limit=1,
            )
            if range_id:
                raise ValidationError(
                    _(
                        "%(name)s is overalapping with range %(age_from)s",
                        name=rec.name,
                        age_from=range_id.name,
                    )
                )
