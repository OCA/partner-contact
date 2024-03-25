from odoo import fields, models


class ResPartnerSequenceType(models.Model):
    _name = "res.partner.sequence.type"
    _description = "Partner Sequence Type"

    name = fields.Char(readonly=True, required=True)
    code = fields.Char(readonly=True)

    sequence_id = fields.Many2one("ir.sequence")
