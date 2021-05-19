# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "tier.validation"]
    _tier_validation_manual_config = False

    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Active"), ("cancel", "Archived")],
        string="Status",
        default="draft",
    )

    @api.model
    def _tier_revalidation_fields(self, values):
        """
        Changing some Partner fields forces Tier Validation to be reevaluated.
        Out of the box these are is_company and parent_id.
        Other can be added extenting this method.
        """
        return ["is_company", "parent_id"]

    @api.model
    def create(self, vals):
        new = super().create(vals)
        if new.need_validation and new.state != "confirmed":
            new.active = False
        else:
            new.active = True
            new.state = "confirmed"
        return new

    def write(self, vals):
        # Changing certain fields required new validation process
        revalidate_fields = self._tier_revalidation_fields(vals)
        if any(x in revalidate_fields for x in vals.keys()):
            self.mapped("review_ids").unlink()
            vals["state"] = "draft"

        # Automatically update active flag depending on state
        if "state" in vals:
            vals["active"] = vals["state"] == "confirmed"
        return super().write(vals)
