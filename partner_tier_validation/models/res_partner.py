# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "tier.validation"]

    _tier_validation_buttons_xpath = "/form/header/field[@name='state']"
    _state_from = ["draft", "cancel"]
    _state_to = ["confirmed"]
    _cancel_state = ["inactive"]
    _tier_validation_manual_config = False

    @api.model
    def _partner_tier_revalidation_fields(self, values):
        """
        Changing some Partner fields forces Tier Validation to be reevaluated.
        Out of the box these are is_company and parent_id.
        Other can be added extending this method.
        """
        # IDEA: make it a System Parameter?
        return [
            "company_type",
            "parent_id",
            "vat",
            "state_id",
            "country_id",
            "property_account_position_id",
            "property_account_receivable_id",
            "property_account_payable_id",
        ]

    def write(self, vals):
        # Changing certain fields requires a new validation process
        revalidate_fields = self._partner_tier_revalidation_fields(vals)
        if any(x in revalidate_fields for x in vals.keys()):
            vals["stage_id"] = self._get_default_stage_id().id
        # Tier Validation does not work with Stages, only States :-(
        # Workaround is to signal state transition adding it to the write values
        if "stage_id" in vals:
            stage_id = vals.get("stage_id")
            stage = self.env["res.partner.stage"].browse(stage_id)
            vals["state"] = stage.state
        res = super().write(vals)
        if "stage_id" in vals and vals.get("stage_id") in self._state_from:
            self.restart_validation()
        return res
