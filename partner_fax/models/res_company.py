from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    fax = fields.Char()
