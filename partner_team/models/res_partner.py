# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    rel_team_ids = fields.One2many("rel.team.partner", "partner_id", string="Teams")
    # team_ids = fields.Many2many(related="rel_team_ids.team_id", string="Teams")
