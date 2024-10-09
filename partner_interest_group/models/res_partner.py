from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    interest_group_ids = fields.Many2many("res.partner.interest.group")
