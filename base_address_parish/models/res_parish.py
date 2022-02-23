# Copyright 2022 Riverminds Cia Ltda - Mamfredy Mejia Matute
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResParish(models.Model):
    _name = "res.parish"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    zip = fields.Char()
    city_id = fields.Many2one("res.city", "City", required=True)
    state_id = fields.Many2one(
        "res.country.state",
        "State",
        readonly=True,
        related="city_id.state_id",
        store=True,
    )
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        readonly=True,
        related="city_id.country_id",
        store=True,
    )

    def name_get(self):
        res = []
        for parish in self:
            name = (
                parish.name if not parish.zip else "%s (%s)" % (parish.name, parish.zip)
            )
            res.append((parish.id, name))
        return res

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += ["|", (self._rec_name, operator, name), ("zip", operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
