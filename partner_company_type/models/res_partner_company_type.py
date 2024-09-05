# Copyright 2017-2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerCompanyType(models.Model):

    _name = "res.partner.company.type"
    _description = "Partner Company Type"

    name = fields.Char(string="Title", required=True, translate=True)
    shortcut = fields.Char(string="Abbreviation", translate=True)

    country_ids = fields.Many2many("res.country", string="Countries")
    state_ids = fields.Many2many(
        "res.country.state",
        string="States",
        domain="[('country_id', 'in', country_ids)]",
    )

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.shortcut:
                name = name + " - " + record.shortcut
            res.append((record.id, name))
        return res

    @api.constrains("name", "shortcut")
    def _check_unique_name_shortcut(self):
        for rec in self:
            if (
                self.env["res.partner.company.type"].search_count(
                    [
                        ("name", "=", rec.name),
                        ("shortcut", "=", rec.shortcut),
                    ]
                )
                > 1
            ):
                if rec.shortcut:
                    raise ValidationError(
                        f"Name ({rec.name}) already exists with this shortcut ({rec.shortcut})!"
                    )
                else:
                    raise ValidationError(f"Name ({rec.name}) already exists!")
