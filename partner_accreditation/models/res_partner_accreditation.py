from odoo import fields, models


class ResPartnerAccreditation(models.Model):
    _name = "res.partner.accreditation"
    _description = "Configurable Accreditation for Partners"

    name = fields.Char(string="Accreditation")
    active = fields.Boolean(default=True)
    partner_ids = fields.Many2many("res.partner")
