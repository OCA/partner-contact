#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_history_ids = fields.One2many(
        comodel_name="partner.name.history",
        inverse_name="partner_id",
        string="Name History",
    )

    def _prepare_name_history_values(self):
        return [
            {
                "partner_id": partner.id,
                "old_name": partner.name,
            }
            for partner in self
        ]

    def write(self, vals):
        if vals.get("name"):
            name_history_values = self._prepare_name_history_values()
            self.env["partner.name.history"].create(name_history_values)
        return super().write(vals)

    def _read(self, field_names):
        partner_name_date = self.env.context.get("partner_name_date")
        use_history_name = partner_name_date and "name" in field_names
        if use_history_name:
            field_names.remove("name")

        res = super()._read(field_names)

        if use_history_name:
            for partner in self:
                history_name = partner.with_context(
                    partner_name_date=None
                )._get_name_at_date(partner_name_date)
                self.env.cache.insert_missing(
                    partner, partner._fields["name"], [history_name]
                )
        return res

    def _get_name_at_date(self, date):
        self.ensure_one()
        history = self.env["partner.name.history"].search(
            [
                ("partner_id", "=", self.id),
                ("change_date", ">=", date),
            ],
            order="change_date asc",
            limit=1,
        )
        return history.old_name if history else self.name
