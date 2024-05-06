# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends_context(
        "show_address",
        "partner_show_db_id",
        "address_inline",
        "show_email",
        "show_vat",
        "lang",
        "no_address_type",
    )
    def _compute_display_name(self):
        super()._compute_display_name()
        if not self._context.get("no_address_type"):
            return
        displayed_types = self._complete_name_displayed_types
        type_description = dict(self._fields["type"]._description_selection(self.env))
        # These filters extracted from def _get_complete_name(self)
        partners = self.filtered(
            lambda partner: not partner.name
            and partner.type in displayed_types
            and (partner.company_name or partner.parent_id)
        )
        for partner in partners:
            name_by_address_type = f", {type_description[partner.type]}"
            partner.display_name = (partner.display_name).replace(
                name_by_address_type, ""
            )
