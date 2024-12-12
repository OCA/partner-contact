from odoo import fields, models


class PartnerTitle(models.Model):
    _inherit = "res.partner.title"

    for_company = fields.Boolean(
        string="For companies", help="Check if the title is meant for companies"
    )
