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
    def create(self, vals):
        new = super().create(vals)
        if new.need_validation and new.state != "confirmed":
            new.active = False
        return new

    def write(self, vals):
        """
        Default `active` is False.
        It is set to True when State changes to confirmed.
        """
        if "state" in vals:
            vals["active"] = vals["state"] == "confirmed"
        return super().write(vals)
