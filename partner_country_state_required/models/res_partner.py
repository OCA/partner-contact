# Copyright 2023 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains("country_id", "state_id")
    def _check_state_required(self):
        if self.env.context.get("no_state_required"):
            return

        for record in self:
            if (
                record.country_id
                and record.country_id.state_required
                and record.country_id.state_ids
                and not record.state_id
            ):
                raise ValidationError(
                    _(
                        "Please specify a state for the address when selecting "
                        "a country with available states."
                    )
                )
