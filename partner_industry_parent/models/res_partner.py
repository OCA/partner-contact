# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api, models


class Partner(models.Model):
    _inherit = "res.partner"

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
        if self._context.get("search_default_industry_id"):
            args.append(
                (
                    "industry_id",
                    "child_of",
                    self._context["search_default_industry_id"],
                )
            )
        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )

    @api.model
    def view_header_get(self, view_id, view_type):
        if self._context.get("industry_id"):
            return _(
                "Partners: %(industry)s",
                industry=self.env["res.partner.industry"]
                .browse(self.env.context["industry_id"])
                .name,
            )
        return super().view_header_get(view_id, view_type)

    def _read_group_industry_id(self, industries, domain, order):
        industry_ids = self.env.context.get("default_industry_id")
        if not industry_ids and self.env.context.get("group_expand"):
            industry_ids = industries._search(
                [], order=order, access_rights_uid=SUPERUSER_ID
            )
        return industries.browse(industry_ids)
