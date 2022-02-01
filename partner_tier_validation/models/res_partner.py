# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "tier.validation"]

    _tier_validation_buttons_xpath = "/form/header/field[@name='state']"
    _state_from = ["draft"]
    _state_to = ["confirmed"]
    _cancel_state = ["inactive"]
    _tier_validation_manual_config = False

    @api.model
    def _tier_revalidation_fields(self, values):
        """
        Changing some Partner fields forces Tier Validation to be reevaluated.
        Out of the box these are is_company and parent_id.
        Other can be added extending this method.
        """
        return ["is_company", "parent_id"]

    @api.model
    def _get_confirmed_stage(self):
        return self.env["res.partner.stage"].search(
            [("state", "in", self._state_to)], limit=1
        )

    @api.model
    def create(self, vals):
        new = super().create(vals)
        # Contact not requiring validation
        # are created in confirmed state
        if not new.need_validation:
            confirmed_stage = self._get_confirmed_stage()
            new.stage_id = confirmed_stage
        return new

    def write(self, vals):
        # Signal state transition by adding to vals
        if "stage_id" in vals:
            stage_id = vals.get("stage_id")
            stage = self.env["res.partner.stage"].browse(stage_id)
            vals["state"] = stage.state
        # Changing certain fields required new validation process
        revalidate_fields = self._tier_revalidation_fields(vals)
        if any(x in revalidate_fields for x in vals.keys()):
            self.mapped("review_ids").unlink()
            vals["state"] = "draft"
            self.request_validation()
        return super().write(vals)
