# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_complete_name(self):
        res = super()._get_complete_name()
        if (
            (self.company_name or self.parent_id)
            and not self.is_company
            and self.env.context.get("_two_lines_partner_address")
        ):
            displayed_types = self._complete_name_displayed_types
            type_description = dict(
                self._fields["type"]._description_selection(self.env)
            )

            name = self.name or ""
            if not name and self.type in displayed_types:
                name = type_description[self.type]
            name = (
                f"{self.commercial_company_name or self.sudo().parent_id.name}\n{name}"
            )
            res = name.strip()
        return res

    @api.depends(
        "complete_name",
        "email",
        "vat",
        "state_id",
        "country_id",
        "commercial_company_name",
    )
    @api.depends_context(
        "show_address",
        "partner_show_db_id",
        "address_inline",
        "show_email",
        "show_vat",
        "lang",
        "_two_lines_partner_address",
    )
    def _compute_display_name(self):  # pylint: disable=W8110
        super()._compute_display_name()
        if self.env.context.get("_two_lines_partner_address"):
            for rec in self:
                name = rec._get_complete_name()
                rec.display_name = name.strip()
        else:
            super()._compute_display_name()
