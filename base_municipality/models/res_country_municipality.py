from odoo import fields, models


class ResCountryMunicipality(models.Model):
    _name = 'res.country.municipality'
    _description = 'Municipality'

    name = fields.Char(required=True)
    country_id = fields.Many2one('res.country', required=True)
    state_id = fields.Many2one('res.country.state')
    code = fields.Char(required=True)

    _sql_constraints = [(
        'name_code_uniq',
        'unique(country_id, state_id, code)',
        'The code of the municipality must be unique by country and state!')]
