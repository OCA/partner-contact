# Copyright 2016 Nicolas Bessi, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    zip_id = fields.Many2one('res.better.zip', 'ZIP Location')

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if not self.zip_id:
            super(ResPartner, self)._onchange_city_id()
        if self.zip_id and self.city_id != self.zip_id.city_id:
            self.zip_id = False
            self.zip = False
            self.city = False
        if self.city_id:
            return {
                'domain': {
                    'zip_id': [('city_id', '=', self.city_id.id)]
                },
            }
        return {'domain': {'zip_id': []}}

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.zip_id and self.state_id != self.zip_id.state_id:
            self.zip_id = False
            self.zip = False
            self.city = False

    @api.onchange('country_id')
    def _onchange_country_id(self):
        res = super(ResPartner, self)._onchange_country_id()
        if self.zip_id and self.zip_id.country_id != self.country_id:
            self.zip_id = False
        return res

    @api.onchange('zip_id')
    def _onchange_zip_id(self):
        if self.zip_id:
            self.country_id = self.zip_id.country_id
            if self.country_id.enforce_cities:
                self.city_id = self.zip_id.city_id
            self.zip = self.zip_id.name
            self.state_id = self.zip_id.state_id
            self.city = self.zip_id.city

    @api.constrains('zip_id', 'country_id', 'city_id', 'state_id')
    def _check_zip(self):
        for rec in self.filtered('zip_id'):
            if rec.zip_id.state_id != rec.state_id:
                raise ValidationError(_(
                    "The state of the partner %s differs from that in "
                    "location %s") % (rec.name, rec.zip_id.name))
            if rec.zip_id.country_id != rec.country_id:
                raise ValidationError(_(
                    "The country of the partner %s differs from that in "
                    "location %s") % (rec.name, rec.zip_id.name))
            if rec.zip_id.city_id != rec.city_id:
                raise ValidationError(_(
                    "The city of partner %s differs from that in "
                    "location %s") % (rec.name, rec.zip_id.name))
