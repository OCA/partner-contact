from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    accreditation_ids = fields.Many2many(
        comodel_name="res.partner.accreditation",
    )
