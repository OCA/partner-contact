from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    accreditation_ids = fields.Many2many("res.partner.accreditation")
