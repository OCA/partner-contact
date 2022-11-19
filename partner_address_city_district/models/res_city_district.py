# Copyright 2022 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCityDistrict(models.Model):
    _name = "res.city.district"
    _description = "City District"

    name = fields.Char(required=True, translate=True)
    city_id = fields.Many2one('res.city', required=True)
    country_id = fields.Many2one(related=['city_id', 'country_id'], readonly=True)
