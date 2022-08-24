from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    municipality_id = fields.Many2one(
        'res.country.municipality',
        domain="[('country_id', '=?', country_id),"
               "('state_id', '=?', state_id)]"
    )
