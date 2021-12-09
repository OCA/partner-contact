# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Partner(models.Model):

    _inherit = "res.partner"

    @api.model
    def _get_default_stage_id(self):
        return self.env["res.partner.stage"].search(
            [("is_default", "=", True)], limit=1
        )

    @api.model
    def _read_group_stage_id(self, states, domain, order):
        return states.search([])

    stage_id = fields.Many2one(
        comodel_name="res.partner.stage",
        group_expand="_read_group_stage_id",
        default=_get_default_stage_id,
        index=True,
        tracking=True,
    )
    state = fields.Selection(related="stage_id.state", store=True, readonly=True)
