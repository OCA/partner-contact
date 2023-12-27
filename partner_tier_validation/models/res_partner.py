# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

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

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """We set the state field in every partner form view."""
        result = super().fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == "form":
            doc = etree.XML(result["arch"])
            node = doc.xpath("//form/sheet")
            if node:
                content = etree.fromstring('<field name="state" invisible="1"/>')
                node[0].addprevious(content)
                new_arch, new_fields = self.env["ir.ui.view"].postprocess_and_fields(
                    doc, self._name
                )
                result["arch"] = new_arch
                # We don't want to loose previous configuration, so, we only want to add
                # the new fields
                new_fields.update(result["fields"])
                result["fields"] = new_fields
        return result
