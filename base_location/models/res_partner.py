# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    zip_id = fields.Many2one('res.city.zip', 'ZIP Location', index=True)
    city_id = fields.Many2one(index=True)  # add index for performance

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if not self.zip_id:
            super()._onchange_city_id()
        if self.zip_id and self.city_id != self.zip_id.city_id:
            self.update({
                'zip_id': False,
                'zip': False,
                'city': False,
            })
        if self.city_id and self.country_enforce_cities:
            return {
                'domain': {
                    'zip_id': [('city_id', '=', self.city_id.id)]
                },
            }
        if self.country_id:
            return {
                'domain': {
                    'zip_id': [('city_id.country_id', '=', self.country_id.id)]
                }
            }
        return {'domain': {'zip_id': []}}

    @api.onchange('country_id')
    def _onchange_country_id(self):
        res = super()._onchange_country_id()
        if self.zip_id and self.zip_id.city_id.country_id != self.country_id:
            self.zip_id = False
        if self.country_id:
            city_zip_domain = {
                "zip_id": [("city_id.country_id", "=", self.country_id.id)]
            }
            if isinstance(res, dict):
                res.setdefault("domain", {})
                res["domain"].update(city_zip_domain)
            else:
                res = {"domain": city_zip_domain}
        return res

    @api.onchange('zip_id')
    def _onchange_zip_id(self):
        if self.zip_id:
            vals = {
                'city_id': self.zip_id.city_id,
                'zip': self.zip_id.name,
                'city': self.zip_id.city_id.name,
            }
            if self.zip_id.city_id.country_id:
                vals.update({'country_id': self.zip_id.city_id.country_id})
            if self.zip_id.city_id.state_id:
                vals.update({'state_id': self.zip_id.city_id.state_id})
            self.update(vals)
        elif not self.country_enforce_cities:
            self.city_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        vals = {}
        if self.state_id.country_id:
            vals.update({'country_id': self.state_id.country_id})
        if self.zip_id and self.state_id != self.zip_id.city_id.state_id:
            vals.update({
                'zip_id': False,
                'zip': False,
                'city': False,
            })
        self.update(vals)
