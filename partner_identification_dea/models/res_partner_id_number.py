# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        if self._context.get("partner_id"):
            args.append(("partner_id", "=", self._context["partner_id"]))
        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.status == "open":
            lines = res.partner_id.id_numbers.filtered(
                lambda l: l.id != res.id and l.category_id == res.category_id
            )
            lines.update({"status": "close"})
        return res

    def write(self, vals):
        if "status" in vals and vals.get("status") == "open":
            lines = self.partner_id.id_numbers.filtered(
                lambda l: l.id != self.id and l.category_id == self.category_id
            )
            lines.update({"status": "close"})
        return super().write(vals)
