# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.fields import Domain


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        if self.env.context.get("partner_id"):
            domain = Domain.AND(
                [domain, [("partner_id", "=", self.env.context["partner_id"])]]
            )
        return super()._search(
            domain, offset=offset, limit=limit, order=order, **kwargs
        )

    def _close_other_open_numbers(self):
        for rec in self:
            rec.partner_id.id_numbers.filtered(
                lambda number, rec=rec: (
                    number.id != rec.id and number.category_id == rec.category_id
                )
            ).status = "close"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.filtered(lambda rec: rec.status == "open")._close_other_open_numbers()
        return records

    def write(self, vals):
        res = super().write(vals)
        if vals.get("status") == "open":
            self._close_other_open_numbers()
        return res
