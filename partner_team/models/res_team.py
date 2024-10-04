# -*- coding: utf-8 -*-

from odoo import fields, models


class Team(models.Model):
    _name = "res.team"
    _inherit = ["image.mixin"]

    def _mailing_get_default_domain(self, mailing):
        return [("list_ids", "in", mailing.partner_ids.ids)]

    active = fields.Boolean(default=True)
    name = fields.Char(
        string="Name of your team",
        required=True,
    )
    rel_team_ids = fields.One2many("rel.team.partner", "team_id", string="Partners")
