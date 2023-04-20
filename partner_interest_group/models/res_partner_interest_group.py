from odoo import fields, models


class ResPartnerInterestGroup(models.Model):
    _name = "res.partner.interest.group"
    _description = "Configurable Interest Group for Partners"

    name = fields.Char(string="Interest Group")
    active = fields.Boolean(default=True)
    partner_id = fields.Many2many("res.partner")
