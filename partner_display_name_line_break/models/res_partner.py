# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

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
            for partner in self:
                displayed_types = partner._complete_name_displayed_types
                type_description = dict(
                    partner._fields["type"]._description_selection(partner.env)
                )
                name = partner.name or ""
                if not name and partner.type in displayed_types:
                    name = type_description[partner.type]
                if name in partner.display_name:
                    pattern = r",\s(?=" + re.escape(name) + ")"
                    partner.display_name = re.sub(pattern, "\n", partner.display_name)
