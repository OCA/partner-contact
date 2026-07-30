# Copyright 2020-2022 Quartile Limited
# Copyright 2025 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    hide_parent = fields.Boolean(
        help="If selected, the parent's name will not be included in the "
        "display name of self."
    )

    def _get_complete_name(self):
        self.ensure_one()
        complete_name = super()._get_complete_name()
        if not self.hide_parent:
            return complete_name

        displayed_types = self._complete_name_displayed_types
        type_description = dict(self._fields["type"]._description_selection(self.env))
        name = self.name or ""
        if self.company_name or self.parent_id:
            if not name and self.type in displayed_types:
                name = type_description.get(self.type, "")
        return name.strip() or complete_name

    # Just add "hide_parent" as a trigger.
    @api.depends(
        "complete_name",
        "email",
        "vat",
        "state_id",
        "country_id",
        "commercial_company_name",
        "hide_parent",
    )
    @api.depends_context(
        "show_address",
        "partner_show_db_id",
        "address_inline",
        "show_email",
        "show_vat",
        "lang",
    )
    def _compute_display_name(self):
        return super()._compute_display_name()
