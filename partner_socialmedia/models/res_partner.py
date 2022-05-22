from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    socialmedia = fields.One2many(
        comodel_name="res.partner.socialmedia",
        inverse_name="partner_id",
        string="Social Media Accounts",
    )