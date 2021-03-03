# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "tier.validation", "mail.activity.mixin"]
    _state_from = ["new", "to approve"]
    _state_to = ["approved"]

    state = fields.Selection(
        [("new", "New"), ("approved", "Approved")], string="Status", default="new"
    )
