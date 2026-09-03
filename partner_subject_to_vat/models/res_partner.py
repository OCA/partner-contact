from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_subject_to_vat = fields.Boolean(string="Is subject to VAT")
