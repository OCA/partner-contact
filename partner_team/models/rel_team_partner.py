from odoo import fields, models


class RelTeamPartner(models.Model):
    _name = "rel.team.partner"

    partner_id = fields.Many2one("res.partner")
    team_id = fields.Many2one("res.team")
    role_ids = fields.Many2many("res.partner.role", string="Roles", required=True)
